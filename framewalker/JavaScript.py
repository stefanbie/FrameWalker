import json
import sys
import time

_driver = None
javaExceptionWaitTime = 10


def set_driver(driver):
    global _driver
    _driver = driver


def execute_script(script, arg=''):
    for x in range(1, javaExceptionWaitTime):
        try:
            return _driver.execute_script(script, arg)
        except Exception as e:
            print('Javascript.execute_script wait ' + str(x) + ' seconds due to ' + str(type(e)))
            time.sleep(1)
    print('Javascript error in ' + sys._getframe().f_code.co_name)
    raise e


def get_timing():
    return json.loads(execute_script("return JSON.stringify(window.performance.timing)"))


def get_resources():
    return json.loads(execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))"))


def get_nbr_of_resources():
    return execute_script("return window.performance.getEntriesByType('resource').length")


def clear_resource_timings():
    execute_script("return window.performance.clearResourceTimings()")


def get_attributes(element):
    return execute_script("var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;", element)


def unix_time_stamp():
    return execute_script("return Date.now()")


def remove_user_properties():
    return execute_script("return localStorage.clear()")

def get_entries_by_type(type):
    return json.loads(execute_script("return JSON.stringify(window.performance.getEntriesByType(arguments[0]))",type))


