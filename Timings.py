import DB
from datetime import datetime
import json
from selenium.common.exceptions import *
import time

driver = None
iteration = 0
transactionTimeStamp = ''
mainNavigationStart = 0
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
    global iteration
    global transaction
    iteration += 1
    transaction = DB.insertTransaction(testCase.id, timeStamp(), transactionName, iteration)
    waitForResourcesLoaded()
    driver.switch_to.default_content()
    saveTimings()
    reportTimingsRecursive("Main")
    driver.execute_script("window.performance.clearResourceTimings()")
    DB.addRelMain(transaction)


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
    frame = DB.insertFrame(transaction.id, driver.current_url)
    entries = getRecources()
    timing = getTiming()
    timing = addRelativeTimes(timing)
    DB.insertRecources(frame.id, entries)
    DB.insertTiming(frame.id, timing)

def addRelativeTimes(timing):
    timing['redirect_time'] = timing['fetchStart']-timing['navigationStart']
    timing['appCache_time'] = timing['domainLookupStart'] - timing['fetchStart']
    timing['DNS_time'] = timing['domainLookupEnd'] - timing['domainLookupStart']
    timing['DNSTCP_time'] = timing['connectStart'] - timing['domainLookupEnd']
    timing['TCP_time'] = timing['connectEnd'] - timing['connectStart']
    timing['blocked_time'] = timing['requestStart'] - timing['connectEnd']
    timing['request_time'] = timing['responseStart'] - timing['requestStart']
    timing['dom_time'] = timing['domComplete'] - timing['responseStart']
    timing['onLoad_time'] = timing['loadEventEnd'] - timing['domComplete']
    timing['total_time'] = timing['loadEventEnd'] - timing['navigationStart']
    return timing

def timeStamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def getRecources():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))

def getTiming():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.timing)"))