import json
import time
import hashlib
from datetime import datetime
from selenium.common.exceptions import *
from framewalker import DB
from framewalker import JavaScript
import csv

_driver = None
transactionTimeStamp = ''
mainNavigationStart = 0
testRun = None
transaction = None
iteration = 0
waitForLoadedTimeOut = 0
waitForLoadedInsterval = 0
verbosity = 0
resourceFilter = []
frameFilter = []
consoleLog = False
CSVlogFilePath = ''


#-----------Init and setters-----------#

def init(driver, _product, _release, _comment, _verbosity=3, _waitForLoadedTimeOut=60, _waitForLoadedInsterval=3, _resourceFilter=None, _frameFilter=None, _consoleLog=False, _CSVlogFilePath=''):
    global testRun
    global _driver
    global waitForLoadedTimeOut
    global waitForLoadedInsterval
    global verbosity
    global resourceFilter
    global frameFilter
    global consoleLog
    global CSVlogFilePath
    _driver = driver
    JavaScript.set_driver(driver)
    verbosity = _verbosity
    if verbosity > 0:
        testRun = DB.insert_test_run(time_stamp(), _product, _release, _comment)
    waitForLoadedTimeOut = _waitForLoadedTimeOut
    waitForLoadedInsterval = _waitForLoadedInsterval
    resourceFilter = _resourceFilter
    frameFilter = _frameFilter
    consoleLog = _consoleLog
    CSVlogFilePath = _CSVlogFilePath
    if CSVlogFilePath != '':
        csv_log_init()


def set_driver(driver):
    global _driver
    _driver = driver
    JavaScript.set_driver(driver)

def set_iteration(iterationNumber):
    global iteration
    iteration = iterationNumber

def increase_iteration():
    global iteration
    iteration += 1

def set_load_interval(loadinterval):
    global waitForLoadedInsterval
    waitForLoadedInsterval = loadinterval

#-----------Main functions-----------#

def report(transactionName):
    global transaction
    if verbosity > 0:
        transaction = DB.insert_transaction(testRun.test_run_id, time_stamp(), transactionName, iteration)
        _driver.switch_to.default_content()
        timing = wait_for_timing_ready()
        save_frame(timing, {'src': _driver.current_url}, '0')
        save_iframes('0')
        JavaScript.clear_resource_timings()
        _driver.switch_to.default_content()
        if not frameFilter is None and len(frameFilter) > 0:
            DB.filter_frames(transaction, frameFilter)
        if DB.transaction_has_frames(transaction):
            DB.add_transaction_times(transaction)
            DB.add_frame_times(transaction)
            DB.add_timing_times(transaction)
            if verbosity > 2:
                if not frameFilter is None and len(resourceFilter) > 0:
                    DB.filter_resources(transaction, resourceFilter)
                DB.add_resource_times(transaction)
        transaction = DB.transaction_by_id(transaction.transaction_id)
        if consoleLog:
            print_console_log()
        if CSVlogFilePath != '':
            print_csv_log(message="")


def save_frame(timing, attributes, frameStructureId):
    src = attributes.get('src')
    if DB.frame_already_exist(testRun, iteration, timing):
        if JavaScript.get_nbr_of_resources() > 0:
            frame = DB.insert_frame(transaction.transaction_id, '{' + frameStructureId + '}', truncated_src(src), hashed_src(src), json.dumps(attributes))
            resources = wait_for_resources_ready(timing)
            save_resources(frame, resources)
    else:
        if src is not None:
            frame = DB.insert_frame(transaction.transaction_id, '{' + frameStructureId + '}', truncated_src(src), hashed_src(src), json.dumps(attributes))
            save_timing(frame, timing)
            if verbosity > 2:
                resources = wait_for_resources_ready(timing)
                save_resources(frame, resources)


def save_iframes(frameStructureId):
    try:
        iFrames = _driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for nbr, iFrame in enumerate(iFrames):
        recFrameStructureId = frameStructureId + "," + str(nbr)
        try:
            attributes = JavaScript.get_attributes(iFrame)
            _driver.switch_to.frame(iFrame)
        except Exception:
            JavaScript.clear_resource_timings()
            return
        timing = wait_for_timing_ready()
        save_frame(timing, attributes, recFrameStructureId)
        JavaScript.clear_resource_timings()
        #currentWindow = _driver.current_window_handle
        save_iframes(recFrameStructureId)
        _driver.switch_to.parent_frame()
        #_driver.switch_to.window(currentWindow)

#-----------Help Functions-----------#

def wait_for_timing_ready():
    time.sleep(1)
    for x in range(1, int(waitForLoadedTimeOut)):
        timing = get_timing()
        connectEnd = timing['loadEventEnd']
        if connectEnd != 0:
            return timing
        time.sleep(1)
    return None


def wait_for_resources_ready(timing):
    if JavaScript.get_nbr_of_resources() == 0:
        return None
    for x in range(1, int(waitForLoadedTimeOut)):
        unixTime = JavaScript.unix_time_stamp()
        resources = get_resources(timing)
        a = max(resources, key=lambda x:x['resource_absolute_end_time'])
        if unixTime - a['resource_absolute_end_time'] > waitForLoadedInsterval*1000:
            return resources
        time.sleep(1)
    return None


def get_timing():
    timing = JavaScript.get_timing()
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


def get_resources(timing):
    resources = JavaScript.get_resources()
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


def save_timing(frame, timing):
    DB.insert_timing(frame.frame_id, timing)


def save_resources(frame, resources):
    DB.insert_recources(frame.frame_id, resources)

#-----------Log-----------#

def print_console_log():
    template = "{0:5}{1:30}{2:10}"
    Red = '\033[91m'
    Black = '\033[90m'
    Yellow = '\033[93m'
    if iteration == 1:
        color = Red
    elif time == -1:
        color = Yellow
    else:
        color = Black
    print(color + template.format(str(transaction.transaction_iteration), transaction.transaction_name, str(transaction.transaction_time)))

def csv_log_init():
    global CSVlogFilePath
    CSVfilename = datetime.now().strftime(r'\log_%Y-%m-%d_%H-%M-%S.csv')
    CSVlogFilePath = CSVlogFilePath + CSVfilename
    with open(CSVlogFilePath, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'transaction', 'iteration', 'elapsed', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def print_csv_log(message):
    with open(CSVlogFilePath, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'transaction', 'iteration', 'elapsed', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'timestamp': transaction.transaction_timestamp, 'transaction': transaction.transaction_name, 'iteration': transaction.transaction_iteration, 'elapsed': transaction.transaction_time, 'message': message})

#-----------Misc-----------#

def hashed_src(src):
    return hashlib.md5(src.encode('utf-8')).hexdigest()[:12]


def truncated_src(src):
    if len(src) > 50:
        src = src[:23] + '....' + src[-23:]
    return src


def time_stamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')