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
waitForLoadedTimeOut = 0
waitForLoadedInsterval = 0
verbosity = 0
resourceFilter = []
frameFilter = []


def init(_driver, _comment, _verbosity=3, _waitForLoadedTimeOut=60, _waitForLoadedInsterval=3, _resourceFilter=None, _frameFilter=None):
    global testCase
    global driver
    global waitForLoadedTimeOut
    global waitForLoadedInsterval
    global verbosity
    global resourceFilter
    global frameFilter
    driver = _driver
    testCase = DB.insertTestCase(timeStamp(), _comment)
    waitForLoadedTimeOut = _waitForLoadedTimeOut
    waitForLoadedInsterval = _waitForLoadedInsterval
    verbosity = _verbosity
    resourceFilter = _resourceFilter
    frameFilter = _frameFilter

def setDriver(_driver):
    global driver
    driver = _driver

def setIteration(iterationNumber):
    global iteration
    iteration = iterationNumber

def increaseIteration():
    global iteration
    iteration += 1

def setLoadInterval(loadinterval):
    global waitForLoadedInsterval
    waitForLoadedInsterval = loadinterval

def report(transactionName):
    global transaction
    print(transactionName)
    print(iteration)
    if verbosity > 0:
        transaction = DB.insertTransaction(testCase.test_case_id, timeStamp(), transactionName, iteration)
        waitForResourcesLoaded()
        driver.switch_to.default_content()
        saveFrame({'src': driver.current_url}, '0')
        saveIFrames('0')
        clearResourceTimings()
        driver.switch_to.default_content()
        if DB.transactionHasFrames(transaction):
            DB.filterFrames(transaction, frameFilter)
            DB.addTransactionTimes(transaction)
            DB.addFrameTimes(transaction)
            DB.addTimingTimes(transaction)
            if verbosity == 3:
                DB.filterResources(transaction, resourceFilter)
                DB.addResourceTimes(transaction)


def timeStamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def saveIFrames(frameStructureId):
    try:
        iFrames = driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for nbr, iFrame in enumerate(iFrames):
        recFrameStructureId = frameStructureId + "," + str(nbr)
        try:
            attributes = getAttributes(iFrame)
            driver.switch_to.frame(iFrame)
        except Exception:
            clearResourceTimings()
            return
        saveFrame(attributes, recFrameStructureId)
        clearResourceTimings()
        currentWindow = driver.current_window_handle
        saveIFrames(recFrameStructureId)
        driver.switch_to.window(currentWindow)


def saveFrame(attributes, frameStructureId):
    src = attributes.get('src')
    timing = getTiming()
    if DB.frameAlreadyExist(testCase, iteration, timing):
        if len(getResources(timing)) > 0:
            frame = DB.insertFrame(transaction.transaction_id, '{' + frameStructureId + '}', truncatedSRC(src), hashedSRC(src), json.dumps(attributes))
            saveResources(frame, timing)
    else:
        if src is not None:
            frame = DB.insertFrame(transaction.transaction_id, '{' + frameStructureId + '}', truncatedSRC(src), hashedSRC(src), json.dumps(attributes))
            timing = saveTiming(frame, timing)
            if verbosity == 3:
                saveResources(frame, timing)


def getTiming():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.timing)"))


def getResources(timing):
    resources = json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))
    res = []
    for d in resources:
        r={}
        r['resource_absolute_start_time'] = int(timing['navigationStart']) + int(d['startTime'])
        r['resource_absolute_end_time'] = r['resource_absolute_start_time'] + int(d['duration'])
        r['resource_time'] = d.pop('duration')
        r['resource_name'] = d.pop('name')
        r['resource_start_time'] = d.pop('startTime')
        del d['entryType']
        res.append(r)
    return res


def saveTiming(frame, timing):
    timing = addRelativeTimingValues(timing)
    DB.insertTiming(frame.frame_id, timing)
    return timing


def saveResources(frame, timing):
    resources = getResources(timing)
    DB.insertRecources(frame.frame_id, resources)


def addRelativeTimingValues(timing):
    timing['timing_redirect'] = timing['fetchStart']-timing['navigationStart']
    timing['timing_appcache'] = timing['domainLookupStart'] - timing['fetchStart']
    timing['timing_dns'] = timing['domainLookupEnd'] - timing['domainLookupStart']
    timing['timing_dnstcp'] = timing['connectStart'] - timing['domainLookupEnd']
    timing['timing_tcp'] = timing['connectEnd'] - timing['connectStart']
    timing['timing_blocked'] = timing['requestStart'] - timing['connectEnd']
    timing['timing_request'] = timing['responseStart'] - timing['requestStart']
    timing['timing_dom'] = timing['domComplete'] - timing['responseStart']
    timing['timing_onload'] = timing['loadEventEnd'] - timing['domComplete']
    timing['timing_time'] = timing['loadEventEnd'] - timing['navigationStart']
    return timing


def getNbrOfResources():
    return driver.execute_script("return window.performance.getEntriesByType('resource').length")


def clearResourceTimings():
    driver.execute_script("window.performance.clearResourceTimings()")


def getAttributes(element):
    return driver.execute_script("var items = {}; "
                                 "for (index = 0; index < arguments[0].attributes.length; ++index) "
                                 "{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; "
                                 "return items;"
                                 , element)


def hashedSRC(src):
    return hashlib.md5(src.encode('utf-8')).hexdigest()[:12]


def truncatedSRC(src):
    if len(src) > 50:
        src = src[:23] + '....' + src[-23:]
    return src


def waitForResourcesLoaded():
    lastNbrOfResources = 0
    for x in range(1, int(waitForLoadedTimeOut/waitForLoadedInsterval)):
        time.sleep(waitForLoadedInsterval)
        nbrOfResources = getNbrOfResources()
        if nbrOfResources > lastNbrOfResources:
            lastNbrOfResources = nbrOfResources
        else:
            break