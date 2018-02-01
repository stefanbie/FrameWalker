import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import IFrame
from framewalker import Timings
from framewalker.JavaScript import execute_script

_driver = None


def driver():
    global _driver
    caps = DesiredCapabilities.INTERNETEXPLORER
    caps['enablePersistentHover'] = False
    _driver = webdriver.Ie(capabilities=caps)
    return _driver


def new_bp():
    global _driver
    if not _driver is None:
        _driver.quit()
        _driver = None
    _driver = driver()
    Timings.set_driver(_driver)
    IFrame.set_driver(_driver)
    Timings.set_iteration(0)
    return _driver


def login(password):
    import autoit
    if autoit.win_exists("Windows Security"):
        autoit.win_activate("Windows Security")
        autoit.win_wait_active("Windows Security", 3)
        autoit.control_send("Windows Security", "[CLASS:Edit; INSTANCE:1]", password)
        autoit.control_click("Windows Security", "OK")


def handle_exception(transaction, exception):
    while len(_driver.window_handles) > 1:
        _driver.switch_to_window(_driver.window_handles[1])
        _driver.close()
        _driver.switch_to_window(_driver.window_handles[0])
    print(transaction + " error")
    if Timings.CSVlogFilePath != '':
        with open(Timings.CSVlogFilePath, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'transaction', 'iteration', 'elapsed', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'timestamp': '', 'transaction': transaction, 'iteration': '', 'elapsed': '', 'message': 'error'})


def click_by_xpath(xpath, timeout=30, throwEx=True):
    try:
        element = WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException as e:
        if throwEx:
            e.msg = "Timeout when trying to click element"
            raise e
        return
    element.click()


def find_by_xpath(xpath, timeout=30):
    element = WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return element


def click_by_id(id):
    return execute_script("return document.getElementById(arguments[0]).click()", id)


def click(element):
    return execute_script("arguments[0].click();", element)


def click_by_xpath_async(xpath, timeout=30):
    element = WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return execute_script("var _e=arguments[0]; setTimeout(function() { _e.click(); }, 100);", element)