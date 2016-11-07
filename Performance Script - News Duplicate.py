import Timings
import IFrame
import DB
import sys
from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

comment = 'News2 1.0 without load with latency.'
verbosity = 3
waitForLoadedTimeOut = 60
waitForLoadedInsterval = 3
numberOfIterations = 20
resourceFilter = []
frameFilter = ['startpage'] #Contains

def Driver():
    return webdriver.Ie()

DB.init()
driver = Driver()
Timings.init(driver, comment, verbosity, waitForLoadedTimeOut, waitForLoadedInsterval, resourceFilter, frameFilter)
IFrame.init(driver)
domainURL = 'https://news-inter-ppe.ikeadt.com'


def handleException(action):
    print(action)
    print(sys.exc_info())

def newBP():
    global driver
    driver.quit()
    driver = None
    driver = Driver()
    Timings.setDriver(driver)
    IFrame.init(driver)
    Timings.setIteration(0)


def js_click_by_id(id):
    driver.execute_script("document.getElementById('%s').click();" % id)


def js_click(element):
    driver.execute_script("arguments[0].click();", element)


def js_click_by_xpath(xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", element)


def click_by_xpath(xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.click()

def BP_01():
    try:
        transaction = 'BP_01_News2Landing'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        action = 'BP_01_ClickGlobalNews'
        #driver.find_element_by_xpath("//div[@id='globalNewsRollup']//a[@id='newsImageLink']").click()
        driver.get('%s/IKEA News/Pages/IKEA-recalls-PATRULL-safety-gates-.aspx' % domainURL)
        Timings.report(action)
    except Exception:
        handleException(action)
def BP_02():
    try:
        transaction = 'BP_01_News2Landing'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_02_ClickPOM'
        js_click_by_xpath("//span[text()='People On The Move']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_02_Changedropdowns'
        click_by_xpath("//select[@id='CountriesFilter']/option[text()='Show All']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_02_ClickFirstResult'
        #js_click_by_xpath("//a[@clicktype='Result'][2]")
        js_click_by_xpath("//a[@href='https://news-inter-ppe.ikeadt.com/PeopleOnTheMove/IKEACommunications/Pages/Henrik-Lagerberg,-new-Retouch-Artist,-IKEA-Communications.aspx']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
def BP_03():
    try:
        transaction = 'BP_01_News2Landing'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_03_ClickIIM'
        js_click_by_xpath("//span[text()='IKEA in the Media']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_03_Changedropdowns'
        click_by_xpath("//select[@id='CountriesFilter']/option[text()='Show All']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_03_ClickTFirstResult'
        #js_click_by_xpath("//a[@clicktype='Result'][1]")
        js_click_by_xpath("//a[@href='https://news-inter-ppe.ikeadt.com/IKEAInTheMedia/Pages/cu-global-IIM-page.aspx']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
def BP_04():
    try:
        transaction = 'BP_01_News2Landing'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_04_ClickNewsletters'
        js_click_by_xpath("//span[text()='Newsletters']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_04_Changedropdowns'
        click_by_xpath("//select[@id='CountriesFilter']/option[text()='Show All']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_04_ClickTFirstResult'
        #js_click(driver.find_elements_by_xpath("//a[@clicktype='Result']")[1])
        js_click(driver.find_element_by_xpath("//a[@href='https://news-inter-ppe.ikeadt.com/Newsletter/Documents/newsltr link cu regression.aspx']"))
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
def BP_05():
    try:
        transaction = 'BP_01_News2Landing'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_05_Search'
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@title='Search...']"))).send_keys('IKEA')
        click_by_xpath("//a[@title='Search']")
        Timings.report(transaction)
    except Exception:
        handleException(transaction)


BPs = [BP_01,
        BP_02,
        BP_03,
        BP_04,
        BP_05,]

for BP in BPs:
    while Timings.iteration < numberOfIterations:
        Timings.increaseIteration()
        BP()
    newBP()