import DB
from datetime import datetime
import json
from selenium.common.exceptions import *
import time

driver = None
iteration = 0
transactionTimeStamp = ''
mainNavigationStart = 0
#startTimes = {}
testCase = None
transaction = None

def init(_driver, testCaseComment):
    global driver
    global testCase
    driver = _driver
    DB.init()
    testCase = DB.insertTestCase(timeStamp(), testCaseComment)


def waitForResourcesLoaded():
    lastNbrOfResources = 0
    while True:
        time.sleep(3)
        nbrOfResources = json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntries().length)"))
        if nbrOfResources > lastNbrOfResources:
            lastNbrOfResources = nbrOfResources
        else:
            break


def getAjaxResources():
    xmlResources = []
    resources = json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntries())"))
    for resource in resources:
        if resource.get("initiatorType") == "xmlhttprequest":
            xmlResources.append(resource)
    return xmlResources


def report(transactionName):
    global transactionTimeStamp
    global iteration
    global transaction
    iteration += 1
    transaction = DB.insertTransaction(testCase.id, timeStamp(), transactionName, iteration)
    #transactionTimeStamp = datetime.now() #.strftime('%Y-%m-%d_%H-%M-%S')
    waitForResourcesLoaded()
    driver.switch_to.default_content()
    saveTimings()
    reportTimingsRecursive("Main")
    driver.execute_script("window.performance.clearResourceTimings()")


def  reportTimingsRecursive(parent):
    '''Itterates all iFrames on the page and report the timings'''
    try:
        iFrames = driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for iFrame in iFrames:
        try:
            driver.switch_to.frame(iFrame)
        except Exception:
            driver.execute_script("window.performance.clearResourceTimings()")
            return
        saveTimings()
        driver.execute_script("window.performance.clearResourceTimings()")
        currentWindow = driver.current_window_handle
        reportTimingsRecursive(iFrame.id)
        driver.switch_to.window(currentWindow)


def saveTimings():
    global driver
    '''Extracts data from browser and decides what is relevant to save'''
    frame = DB.insertFrame(transaction.id, driver.current_url)
    entries = getRecources()
    timing = getTiming()
    DB.insertRecources(frame.id, entries)
    DB.insertTiming(frame.id, timing)


def timeStamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def getRecources():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))

def getTiming():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.timing)"))