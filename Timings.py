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


def init(_driver, _comment, _verbosity=3, _waitForLoadedTimeOut=60, _waitForLoadedInsterval=3):
    global testCase
    global driver
    global waitForLoadedTimeOut
    global waitForLoadedInsterval
    global verbosity
    driver = _driver
    testCase = DB.insertTestCase(timeStamp(), _comment)
    waitForLoadedTimeOut = _waitForLoadedTimeOut
    waitForLoadedInsterval = _waitForLoadedInsterval
    verbosity = _verbosity


def increaseIteration():
    global iteration
    iteration += 1


def report(transactionName):
    global transaction
    if verbosity > 0:
        transaction = DB.insertTransaction(testCase.test_case_id, timeStamp(), transactionName, iteration)
        waitForResourcesLoaded()
        driver.switch_to.default_content()
        saveFrame({'src': driver.current_url}, '0')
        saveIFrams('0')
        clearResourceTimings()
        if DB.transactionHasFrames(transaction):
            DB.addTransactionTimes(transaction)
            DB.addFrameTimes(transaction)
            DB.addTimingTimes(transaction)
            if verbosity == 3:
                DB.addResourceTimes(transaction)


def timeStamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def saveIFrams(frameStructureId):
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
        saveIFrams(recFrameStructureId)
        driver.switch_to.window(currentWindow)


def saveFrame(attributes, frameStructureId):
    timing = getTiming()
    if not DB.frameAlreadyExist(testCase, iteration, timing) | (verbosity == 3 & (len(json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))) > 0)):
        src = attributes.get('src')
        if not src is None and src.startswith('http'):
            frame = DB.insertFrame(transaction.transaction_id, '{' + frameStructureId + '}', truncatedSRC(src), hashedSRC(src), json.dumps(attributes))
            timing = saveTiming(frame, timing)
            if verbosity == 3:
                saveResources(timing, frame)


def getTiming():
    return json.loads(driver.execute_script("return JSON.stringify(window.performance.timing)"))


def getResources(timing):
    resources = json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))
    for d in resources:
        d['resource_absolute_start_time'] = int(timing['navigationStart']) + int(d['startTime'])
        d['resource_absolute_end_time'] = d['resource_absolute_start_time'] + int(d['duration'])
        d['resource_time'] = d.pop('duration')
        d['resource_name'] = d.pop('name')
        d['resource_start_time'] = d.pop('startTime')
        del d['entryType']
    return resources


def saveTiming(frame, timing):
    timing = addRelativeTimingValues(timing)
    DB.insertTiming(frame.frame_id, timing)
    return timing


def saveResources(timing, frame):
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
    src = src.split('/')[2]
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