import Timings
import IFrame
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = None

def Driver():
    caps = DesiredCapabilities.INTERNETEXPLORER
    caps['enablePersistentHover'] = False
    driver = webdriver.Ie(capabilities=caps)
    return driver

def newBP():
    global driver
    if not driver is None:
        driver.quit()
        driver = None
    driver = Driver()
    Timings.setDriver(driver)
    IFrame.setDriver(driver)
    Timings.setIteration(0)
    return driver

def click_by_xpath(xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.click()

def js_click_by_id(id):
    driver.execute_script("document.getElementById('%s').click();" % id)


def js_click(element):
    driver.execute_script("arguments[0].click();", element)


def js_click_by_xpath(xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", element)

def js_click_by_xpath_async(xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("var _e=arguments[0]; setTimeout(function() { _e.click(); }, 100);", element)

def handleException(transaction):
    print('Exception in ' + transaction)
