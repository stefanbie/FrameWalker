from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from framewalker import DB, Timings

domainURL = 'http://systemverification.com'

caps = DesiredCapabilities.INTERNETEXPLORER
caps['enablePersistentHover'] = False
driver = webdriver.Ie(capabilities=caps)

DB.init(_schemaName='framewalker', _host='127.0.0.1', _port=3306, _user='dbuser', _password='dbuser')
Timings.init(_driver=driver, _product='SysVer', _release='1', _comment='test', _verbosity=3, _waitForLoadedTimeOut=60, _waitForLoadedInsterval=3, _resourceFilter=[], _frameFilter=[])


transaction = 'hem'
driver.get('%s/en' % domainURL)
Timings.report(transaction)
driver.quit()