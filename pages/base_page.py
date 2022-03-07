'''
THE SCRIPT CONTAINS THE METHODS TO BE USED IN THE TESTS - PAGE CLASSES INHERIT THE BasePage CLASS
'''

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    # driver passed into Base page from parent
    def __init__(self, driver):
        self.driver = driver

    # confirm page title
    def check_page_title(self, title):
        WebDriverWait(self.driver, 10).until(ec.title_is(title))

    # actions
    def click(self, by_locator):
        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator)).click()

    def send_keys_entry(self, by_locator, text):
        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator)).send_keys(text)

    # move mouse to middle of the element, use for elements w/ hover actions, positioning etc.
    # check content after hovering over element
    def hover_over_element(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator))
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        # performs all stored actions
        actions.perform()

    def check_if_enabled(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator),"element {} not visible ".format(by_locator[1]))
        return bool(element)

    def check_for_return_element(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator),"element {} not visible ".format(by_locator[1]))
        return element

    def return_element_text(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator),"element {} not visible ".format(by_locator[1]))
        return element.text

    def get_title(self, title):
        element = WebDriverWait(self.driver, 10).until(ec.title_is(title),"element {} not visible ".format(by_locator[1]))
        return element.text

    def return_css_property_value(self, by_locator, key):
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(by_locator),"element {} not visible ".format(by_locator[1]))
        value = element.value_of_css_property(key)
        return value
