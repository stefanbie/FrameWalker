from selenium.common.exceptions import NoSuchElementException
_driver = None
elementFound = False


def set_driver(driver):
    global _driver
    _driver = driver


def set_by_xpath(elementPath):
    '''Sets the driver to point at the first iFrame where element xPath is found'''
    global elementFound
    _driver.switch_to.default_content()
    elementFound = False
    if check_exists_by_xpath(elementPath):
        return True
    else:
        set_frame_recursive(elementPath)
        return elementFound


def set_frame_recursive(elementPath):
    '''Recursively finds and sets the driver to point at the first iFrame where element xPath is found'''
    global elementFound
    if elementFound: return
    try:
        iFrames = _driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for iFrame in iFrames:
        try:
            _driver.switch_to.frame(iFrame)
        except Exception:
            return
        if check_exists_by_xpath(elementPath):
            elementFound = True
            return
        else:
            currentWindow = _driver.current_window_handle
            set_frame_recursive(elementPath)
            _driver.switch_to.window(currentWindow)
    return


def check_exists_by_xpath(xpath):
    '''Checks if the xpath is present in current iFrame'''
    try:
        _driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True