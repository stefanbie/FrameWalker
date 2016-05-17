import Timings
import IFrame
import DB
from selenium import webdriver


DB.init()
driver = webdriver.Chrome()
Timings.init(driver, _comment='Google Version 1.0', _verbosity=2, _waitForLoadedTimeOut=60, _waitForLoadedInsterval=3)
IFrame.init(driver)


while(True):
    Timings.increaseIteration()

    driver.get('https://mail.google.com')
    Timings.report('TR_01_mail')

    driver.get('https://translate.google.com')
    Timings.report('TR_02_translate')

