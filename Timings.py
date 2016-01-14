import DB
from datetime import datetime
import json
from selenium.common.exceptions import *
import time

driver = None
transactionTimeStamp = ''
mainNavigationStart = 0
testCase = None
transaction = None
iteration = 0
waitForLoadedTimeOut = 60
waitForLoadedInsterval = 3

def init(_driver, testCaseComment):
    global driver
    global testCase
    driver = _driver
    DB.init()
    testCase = DB.insertTestCase(timeStamp(), testCaseComment)


def increaseIteration():
    global iteration
    iteration += 1


def waitForResourcesLoaded():
    lastNbrOfResources = 0
    for x in range(1, int(waitForLoadedTimeOut/waitForLoadedInsterval)):
        time.sleep(waitForLoadedInsterval)
        nbrOfResources = getNbrOfResources()
        if nbrOfResources > lastNbrOfResources:
            lastNbrOfResources = nbrOfResources
        else:
            break


def report(transactionName):
    global transaction
    transaction = DB.insertTransaction(testCase.id, timeStamp(), transactionName, iteration)
    waitForResourcesLoaded()
    driver.switch_to.default_content()
    frame = saveFrame({'src': driver.current_url}, 0)
    reportTimingsRecursive(frame)
    clearResourceTimings()
    DB.addRelMain(transaction)


def  reportTimingsRecursive(parentFrame):
    '''Itterates all iFrames on the page and report the timings'''
    try:
        iFrames = driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for iFrame in iFrames:
        try:
            attributes = getAttributes(iFrame)
            driver.switch_to.frame(iFrame)
        except Exception:
            clearResourceTimings()
            return
        if not attributes.get('src') is None and attributes.get('src').startswith('http'):
            frame = saveFrame(attributes, parentFrame.id)
        else:
            frame = parentFrame
        clearResourceTimings()
        currentWindow = driver.current_window_handle
        reportTimingsRecursive(frame)
        driver.switch_to.window(currentWindow)


def saveFrame(attributes, parentID):
    src = attributes.get('src')
    if len(src) > 50:
        src = src[:23] + '....' + src[-23:]
    frame = DB.insertFrame(transaction.id, parentID, src, json.dumps(attributes))
    saveTiming(frame)
    saveResources(frame)
    return frame


def saveTiming(frame):
    timing = getTiming()
    timing = addRelativeTimes(timing)
    DB.insertTiming(frame.id, timing)


def saveResources(frame):
    entries = getRecources()
    for d in entries:
        del d['entryType']
    DB.insertRecources(frame.id, entries)


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


def getNbrOfResources():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntries().length)"))


def getRecources():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))


def clearResourceTimings():
    driver.execute_script("window.performance.clearResourceTimings()")


def getTiming():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.timing)"))


def getAttributes(element):
    return driver.execute_script("var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;", element)


def setWaitForLoadedTimeOut(wait):
    global waitForLoadedTimeOut
    waitForLoadedTimeOut = wait


def setWaitForLoadedInsterval(interval):
    global waitForLoadedInsterval
    waitForLoadedInsterval = interval