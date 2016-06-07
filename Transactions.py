import Timings
import IFrame
import DB
from selenium import webdriver


comment = 'Google Version 1.0'
verbosity = 3
waitForLoadedTimeOut = 60
waitForLoadedInsterval = 3
resourceFilter = []
frameFilter = []


DB.init()
driver = webdriver.Chrome()
Timings.init(driver, _comment=comment, _verbosity=verbosity, _waitForLoadedTimeOut=waitForLoadedTimeOut, _waitForLoadedInsterval=waitForLoadedInsterval, _resourceFilter=resourceFilter, _frameFilter=frameFilter)
IFrame.init(driver)


while(True):
    Timings.increaseIteration()

    driver.get('https://mail.google.com')
    Timings.report('TR_01_mail')

    driver.get('https://translate.google.com/')
    Timings.report('TR_02_translate')
