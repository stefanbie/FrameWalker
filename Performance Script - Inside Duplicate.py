import Timings
import IFrame
import DB
import sys
import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

comment = 'Test'
verbosity = 3
waitForLoadedTimeOut = 60
waitForLoadedInsterval = 3
numberOfIterations = 20
resourceFilter = ['https://app-6de7872b7b8ec7.spapps.inside-ppe.ikeadt.com/IKEAInsideMoveAppsPopup/Scripts/popup_ext.js']
frameFilter = ['startpage']  # Contains

def Driver():
    return webdriver.Ie()

DB.init()
driver = Driver()
Timings.init(driver, comment, verbosity, waitForLoadedTimeOut, waitForLoadedInsterval, resourceFilter, frameFilter)
IFrame.init(driver)
domainURL = 'https://intranet-inter-ppe.ikeadt.com'

def handleException(transaction):
    print(transaction)
    print(sys.exc_info())
def js_click(element):
    driver.execute_script("arguments[0].click();", element)
def js_click_by_id(id):
    driver.execute_script("document.getElementById('%s').click();" % id)

bookingsMap = {
    'calenderTable': "//div[@id='ctl00_ctl53_g_34b556db_1a45_4aa1_92e0_5a043d2c9680_ctl01_ctl00_ctl00']",
    'calenderAdd': "//div[@id='ctl00_ctl53_g_34b556db_1a45_4aa1_92e0_5a043d2c9680_ctl01_ctl00_ctl00']/div/table/tbody/tr/td/a",
    'userFieldActivation': "//div[contains(@id, '_UserField_upLevelDiv')]",
    'userField': "//span[contains(@id, '_UserField')]",
    'checkNames': "//a[contains(@id, '_UserField_checkNames')]/img",
    'fromDate': "//input[contains(@id, '_ctl00_ctl05_ctl02_ctl00_ctl00_ctl04_ctl00_ctl00_DateTimeField_DateTimeFieldDate')]",
    'toDate': "//input[contains(@id, '_ctl00_ctl05_ctl03_ctl00_ctl00_ctl04_ctl00_ctl00_DateTimeField_DateTimeFieldDate')]",
    'addSelectedResource': "//button[contains(@id, '_AddButton')]",
    'save': "//input[contains(@id, '_ctl00_ctl00_diidIOSaveItem')]",
    'selectedCreatedBooking': "//div[contains(@class, 'ms-acal-item')]",
    'delete': "//a[@id='Ribbon.Calendar.Events.Manage.Delete-Medium']"
}

def newBP():
    global driver
    driver.quit()
    driver = None
    driver = Driver()
    Timings.setDriver(driver)
    IFrame.init(driver)
    Timings.setIteration(0)

def BP_02():
    try:
        transaction = 'BP_02_SellingMarketing'
        driver.get('%s/sellingmarketing/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_02_HeaderWP'
        IFrame.setByXpath("//span[contains(text(),'External Media Swedish')]")
        driver.find_element_by_xpath("//span[contains(text(),'External Media Swedish')]").click()
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_02_SellingMarketing'
        driver.get('%s/sellingmarketing/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
        handleException(transaction)
    try:
        transaction = 'BP_02_HeaderSublinksWP'
        IFrame.setByXpath("//a[contains(text(),'test global link swedish')]")
        driver.find_element_by_xpath("//a[contains(text(),'test global link swedish')]").click()
        driver.switch_to_window(driver.window_handles[1])
        Timings.report(transaction)
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    except Exception:
        handleException(transaction)
def BP_03():
    try:
        transaction = 'BP_03_VisionCulture'
        driver.get('%s/aboutikea/VisionCulture/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
    try:
        transaction = 'BP_03_Stories'
        driver.get('%s/aboutikea/VisionCulture/Coworkerstories/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_04():
    try:
        transaction = 'BP_04_IKEATrustline'
        driver.get('%s/aboutikea/IKEATrustLine/Pages/default.aspx' % domainURL)
        Timings.report(transaction)

        transaction = 'BP_04_ChangeValues'
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[1]"))
        select = Select(driver.find_element_by_xpath("//select[@id='ddlCountry']"))
        select.select_by_visible_text("Show All")
        Timings.report(transaction)

        transaction = 'BP_04_RedirectBasicPage'
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[1]"))
        driver.find_element_by_xpath("//a[contains(text(),'Switzerland')]").click()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_05():
    try:
        transaction = 'BP_05_QAPage'
        driver.get('%s/insidehelp/QALoginpassword/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_06():
    try:
        transaction = 'BP__06_SectionSite'
        driver.get('%s/methodsstrategies/RoutinesWorkingMethods/SupplyingLogistics/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
    try:
        transaction = 'BP__06_RecentUpdates'
        IFrame.setByXpath("//a[contains(text(),'Shipping Guides')]")
        driver.find_element_by_xpath("//a[contains(text(),'Shipping Guides')]").click()
        driver.switch_to_window(driver.window_handles[1])
        Timings.report(transaction)
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    except Exception:
        handleException(transaction)
def BP_08():
    try:
        transaction = 'BP_08_AboutIKEA'
        driver.get('%s/aboutikea' % domainURL) # Redirect to: /aboutikea/Pages/default.aspx
        Timings.report(transaction)

        transaction = 'BP_08_IKEASearch'
        driver.find_element_by_xpath("//input[@title='Search Inside']").send_keys("IKEA")
        driver.find_element_by_xpath("//a[@title='Search']").click()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_12():
    try:
        transaction = 'BP_12_StartPage'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
        IFrame.setByXpath("//a[@title='Stäng dialogruta']")
        driver.find_element_by_xpath("//a[@title='Stäng dialogruta']").click()
    except Exception:
        handleException(transaction)

        transaction = 'BP_12_Click'
        element = driver.find_element_by_xpath("//span[contains(text(),'useful contact 4')]")
        js_click(element)
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_13():
    try:
        transaction = 'BP_12_StartPage'
        driver.get('%s/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
        IFrame.setByXpath("//a[@title='Stäng dialogruta']")
        driver.find_element_by_xpath("//a[@title='Stäng dialogruta']").click()

        transaction = 'BP_13_Sitemap'
        IFrame.setByXpath("//img[@class='siteMapImg']")
        driver.find_element_by_xpath("//img[@class='siteMapImg']").click()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_14():
    try:
        Timings.setLoadInterval(1)
        transaction = 'BP_14_PhotoCategory'
        driver.get('%s/methodsstrategies/Strategies/Qualitystrategy/FutureSearchforQuality/Pages/default.aspx' % domainURL)
        Timings.report(transaction)
        Timings.setLoadInterval(waitForLoadedInsterval)

        transaction = 'BP_14_Forward'
        IFrame.setByXpath("//button[@id='cboxNext']")
        js_click_by_id('cboxSlideshow') # Pause
        driver.find_element_by_xpath("//button[@id='cboxNext']").click()
        Timings.report(transaction)

        transaction = 'BP_14_ForwardAgain'
        IFrame.setByXpath("//button[@id='cboxNext']")
        driver.find_element_by_xpath("//button[@id='cboxNext']").click()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_15():
    try:
        transaction = 'BP_15_PhotoAlbumSite'
        driver.get('%s/photos' % domainURL)
        Timings.report(transaction)

        transaction = 'BP_15_Paging'
        IFrame.setByXpath("//a[contains(@class,'fg-button ui-button ui-state-default') and text()='2']")
        driver.find_element_by_xpath("//a[contains(@class,'fg-button ui-button ui-state-default') and text()='2']").click()
        Timings.report(transaction)

        transaction = 'BP_15_OpenAlbum'
        driver.switch_to.default_content()
        IFrame.setByXpath("//input[contains(@title,'Search for albums')]")
        driver.find_element_by_xpath("//input[contains(@title,'Search for albums')]").send_keys("Visite Peter")
        driver.find_element_by_xpath("//a[contains(text(),'Visite Peter')]").click()
        Timings.report(transaction) # Is this name correct?

        transaction = 'BP_15_ClickImage'
        driver.find_element_by_xpath("//a[@id='Tile_WPQ1_1_3']").click()
        Timings.report(transaction)

        transaction = 'BP_15_ClickForwardArrow'
        IFrame.setByXpath("//button[@id='cboxNext']")
        js_click_by_id('cboxNext')
        driver.switch_to.default_content()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_16():
    try:
        transaction = 'BP_16_CalendarLandingSite'
        driver.get('%s/calendar' % domainURL)
        Timings.report(transaction)

        transaction = 'BP_16_ClickCalendarName'
        IFrame.setByXpath("//input[@type='search']")
        driver.find_element_by_xpath("//input[@type='search']").send_keys('STMS Global Rollout Project')
        IFrame.setByXpath("//*[@id='CalendarList']/tr/td[1]/a")
        driver.find_element_by_xpath("//*[@id='CalendarList']/tr/td[1]/a").click()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)
def BP_17():
    try:
        transaction = 'BP_17_ForMyJobPage'
        driver.get('%s/pages/formyjob.aspx' % domainURL)
        Timings.report(transaction)

        transaction = 'BP_17_ShowAll'
        IFrame.setByXpath("//a[@class='seeAllMessage']")
        js_click(driver.find_element_by_xpath("//a[@class='seeAllMessage']"))
        driver.switch_to_window(driver.window_handles[1])
        Timings.report(transaction)

        transaction = 'BP_17_ChangeFilters1'
        IFrame.setByXpath("//select[@id='ddlCountry']")
        select = Select(driver.find_element_by_xpath("//select[@id='ddlCountry']"))
        select.select_by_visible_text("Show All")
        Timings.report(transaction)

        transaction = 'BP_17_ChangeFilters2'
        IFrame.setByXpath("//select[@id='ddlJob']")
        select = Select(driver.find_element_by_xpath("//select[@id='ddlJob']"))
        select.select_by_visible_text("Show All")
        driver.switch_to.default_content()
        Timings.report(transaction)

        transaction = 'BP_17_NewMessage'
        IFrame.setByXpath("//span[text()='Message 1']/..")
        js_click(driver.find_element_by_xpath("//span[text()='Message 1']/.."))
        #driver.switch_to.default_content()
        #time.sleep(5)
        driver.switch_to_window(driver.window_handles[2])
        Timings.report(transaction)

        driver.close()
        driver.switch_to_window(driver.window_handles[1])
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

    except Exception:
         handleException(transaction)
def BP_18():
    try:
        transaction = 'BP_18_ResourceBookingSite'
        driver.get('%s/resbook' % domainURL)
        Timings.report(transaction)

        transaction = 'BP_18_ClickAdd'
        driver.find_element_by_xpath(bookingsMap['calenderTable']).click()
        time.sleep(2)
        driver.find_element_by_xpath(bookingsMap['calenderAdd']).click()
        time.sleep(2)
        Timings.report(transaction)

        transaction = 'BP_18_AddAttendees'

        IFrame.setByXpath(bookingsMap['userFieldActivation'])
        driver.find_element_by_xpath(bookingsMap['userFieldActivation']).click()
        webdriver.ActionChains(driver).send_keys("Tstpetese3001;Tstpetese3003;Tstpetese3004;Tstpetese3005;Tstpetese3006;Tstpetese3007").perform()
        # Check names
        driver.find_element_by_xpath(bookingsMap['checkNames']).click()
        Timings.report(transaction)

        transaction = 'BP_18_SelectedDateAndTime'
        IFrame.setByXpath(bookingsMap['fromDate'])
        # Enter dates
        _us_date = datetime.date.today().strftime('%d/%m/%Y')
        driver.find_element_by_xpath(bookingsMap['fromDate']).clear()
        driver.find_element_by_xpath(bookingsMap['fromDate']).send_keys(_us_date)
        driver.find_element_by_xpath(bookingsMap['toDate']).clear()
        driver.find_element_by_xpath(bookingsMap['toDate']).send_keys(_us_date)
        Timings.report(transaction)

        transaction = 'BP_18_SelectResourcelist'
        IFrame.setByXpath("//select[@title='Resources possible values']")
        select = Select(driver.find_element_by_xpath("//select[@title='Resources possible values']"))
        select.select_by_value('2')

        # Add the resource
        driver.find_element_by_xpath(bookingsMap['addSelectedResource']).click()
        Timings.report(transaction)

        # Save
        transaction = 'BP_18_ClickSave'
        IFrame.setByXpath(bookingsMap['save'])
        driver.find_element_by_xpath(bookingsMap['save']).click()
        Timings.report(transaction)

        # Clean up
        IFrame.setByXpath(bookingsMap['selectedCreatedBooking'])
        _e = driver.find_element_by_xpath(bookingsMap['selectedCreatedBooking'])
        driver.execute_script("arguments[0].click();", _e)
        # Delete meeting
        time.sleep(2)
        driver.find_element_by_xpath(bookingsMap['delete']).click()
        # Confirm delete
        driver.switch_to.alert.accept()
        time.sleep(3)
    except Exception:
        handleException(transaction)
def BP_19():
    try:
        transaction = 'BP_19_EventBookingLandingPage'
        driver.get('%s/eventbooking' % domainURL)
        Timings.report(transaction)

        transaction = 'BP_19_OpenEvent'
        IFrame.setByXpath("//td[contains(text(),'Event 1')]/../td/a[contains(text(),'Edit')]")
        driver.find_element_by_xpath("//td[contains(text(),'Event 1')]/../td/a[contains(text(),'Edit')]").click()
        Timings.report(transaction)
    except Exception:
         handleException(transaction)

BPs = [BP_02,
        BP_03,
        BP_04,
        BP_05,
        BP_06,
        BP_08,
        BP_12,
        BP_13,
        BP_14,
        BP_15,
        BP_16,
        BP_17,
        BP_18,
        BP_19]

for BP in BPs:
    while Timings.iteration < numberOfIterations:
        Timings.increaseIteration()
        BP()
    newBP()