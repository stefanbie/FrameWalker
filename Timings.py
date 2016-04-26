import DB
from datetime import datetime
import json
from selenium.common.exceptions import *
import time
import hashlib

driver = None
transactionTimeStamp = ''
mainNavigationStart = 0
testCase = None
transaction = None
iteration = 0
waitForLoadedTimeOut = 60
waitForLoadedInsterval = 3

def init(_driver, testCaseComment):
    global testCase
    global driver
    global testcase_timestamp
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
    transaction = DB.insertTransaction(testCase.test_case_id, timeStamp(), transactionName, iteration)
    waitForResourcesLoaded()
    driver.switch_to.default_content()
    saveFrame({'src': driver.current_url}, '0')
    saveIFrams('0')
    clearResourceTimings()
    DB.addTransactionTimes(transaction)
    DB.addFrameTimes(transaction)
    DB.addTimingTimes(transaction)
    DB.addResourceTimes(transaction)

def  saveIFrams(frid):
    '''Itterates all iFrames on the page and report the timings'''
    try:
        iFrames = driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for nbr, iFrame in enumerate(iFrames):
        recFrid = frid + "," + str(nbr)
        try:
            attributes = getAttributes(iFrame)
            driver.switch_to.frame(iFrame)
        except Exception:
            clearResourceTimings()
            return
        saveFrame(attributes, recFrid)
        clearResourceTimings()
        currentWindow = driver.current_window_handle
        saveIFrams(recFrid)
        driver.switch_to.window(currentWindow)


def saveFrame(attributes, frid):
    src = attributes.get('src')
    if not src is None and src.startswith('http'):
        frame = DB.insertFrame(transaction.transaction_id, '{' + frid + '}', truncatedSRC(src), hashedSRC(src), json.dumps(attributes))
        timing = getTiming()
        resources = getResources(timing)
        saveTiming(frame)
        saveResources(resources, frame)


def hashedSRC(src):
    return hashlib.md5(src.encode('utf-8')).hexdigest()[:12]


def truncatedSRC(src):
    src = src.split('/')[2]
    if len(src) > 50:
        src = src[:23] + '....' + src[-23:]
    return src


def saveTiming(frame):
    timing = getTiming()
    timing = addRelativeTimingValues(timing)
    DB.insertTiming(frame.frame_id, timing)
    return timing


def saveResources(resources, frame):
    DB.insertRecources(frame.frame_id, resources)


def addRelativeTimingValues(timing):
    timing['redirect_time'] = timing['fetchStart']-timing['navigationStart']
    timing['appcache_time'] = timing['domainLookupStart'] - timing['fetchStart']
    timing['dns_time'] = timing['domainLookupEnd'] - timing['domainLookupStart']
    timing['dnstcp_time'] = timing['connectStart'] - timing['domainLookupEnd']
    timing['tcp_time'] = timing['connectEnd'] - timing['connectStart']
    timing['blocked_time'] = timing['requestStart'] - timing['connectEnd']
    timing['request_time'] = timing['responseStart'] - timing['requestStart']
    timing['dom_time'] = timing['domComplete'] - timing['responseStart']
    timing['onload_time'] = timing['loadEventEnd'] - timing['domComplete']
    timing['timing_time'] = timing['loadEventEnd'] - timing['navigationStart']
    return timing


def timeStamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def getResources(timing):
    resources = json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))

    for d in resources:
        d['absolute_start_time'] = int(timing['navigationStart']) + int(d['startTime'])
        d['absolute_end_time'] = d['absolute_start_time'] + int(d['duration'])
        d['resource_time'] = d.pop('duration')
        del d['entryType']
    return resources

def getNbrOfResources():
    return driver.execute_script("return window.performance.getEntriesByType('resource').length")


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