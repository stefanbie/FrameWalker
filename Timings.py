import csv
from datetime import datetime
import json
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import os
import time

driver = None
logTimeStamp = ''
iteration = 0
transaction = ''
day = ''
transactionTimeStamp = ''
logFileDir = ''
logFilePath = ''
frameList = []
sleepBeforeReport = 0
ajax = False
mainNavigationStart = 0
startTimes = {}

def init(_driver, _logFileDir, _sleepBeforeReport):
    global driver
    global logFileDir
    global sleepBeforeReport
    driver = _driver
    logFileDir = _logFileDir
    sleepBeforeReport = _sleepBeforeReport
    setLogFilePath()

def jsonWrite(timing):
    print(timing)

def setLogFilePath():
    '''Sets tha path to the log file'''
    global logTimeStamp
    global day
    global logFilePath
    timeStamp = datetime.now()
    if timeStamp.strftime('%Y-%m-%d_%H-%M-%S')[8:10] != day:
        logTimeStamp = timeStamp.strftime('%Y-%m-%d_%H-%M-%S')
        day = logTimeStamp[8:10]
        logFilePath = logFileDir + '\\' + logTimeStamp + '.csv'


def report(_transaction):
    global frameList
    global transactionTimeStamp
    global iteration
    global transaction
    transaction = _transaction
    transactionTimeStamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    iteration += 1
    time.sleep(sleepBeforeReport)

    driver.switch_to.default_content()
    timing = saveTimings()
    jsonWrite(timing)
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
        except StaleElementReferenceException:
            driver.execute_script("window.performance.clearResourceTimings()")
            return
        timings = saveTimings()
        driver.execute_script("window.performance.clearResourceTimings()")
        currentWindow = driver.current_window_handle
        reportTimingsRecursive(iFrame.id)
        driver.switch_to.window(currentWindow)

def saveTimings():
    '''Extracts data from browser and decides what is relevant to save'''
    global frameList
    global ajax
    global startTimes
    global mainNavigationStart

    timing = json.loads(driver.execute_script("return JSON.stringify(window.performance.timing)"))
    entries = json.loads(driver.execute_script("return JSON.stringify(window.performance.getEntries())"))

    return timing
