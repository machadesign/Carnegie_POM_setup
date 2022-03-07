'''
CONTEST FILE CONTAINS FIXTURES ACCESSIBLE TO TESTS IN CLASSES/MODULES WITHIN THE SAME DIRECTORY
THE ARGUMENTS FOR THE FIXTURES IN THE CONFTEST FILE ARE SPECIFIED IN THE CONFIGURATION FILE
'''


import yaml
import pytest
import re
from selenium import webdriver
import config_verification
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireService
# With selenium4 as the key executable_path is deprecated you have to use an instance of the Service() class

with open("/Users/matthewchadwell/PycharmProjects/Automation_setup/configuration.yaml") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

browser_device_list = data["BROWSER_PARAMS"]
chrome_path_exe = data["BROWSER_EXE_PATHS"]["CHROME"]
firefox_path_exe = data["BROWSER_EXE_PATHS"]["FIREFOX"]
safari_path_exe = data["BROWSER_EXE_PATHS"]["SAFARI"]
# 

Cservice = ChromeService(executable_path=chrome_path_exe)
Fservice = FireService(executable_path=firefox_path_exe)
# Safari does not utilize the instance of the Service class


@pytest.hookimpl()
def pytest_sessionstart(session):
    # check the configuration.yaml for the expected browser settings
    config_verification.check_settings(data)

def check_device_list_for_device_type(request_param):
    # Checks if browser specified in the configuration file is for desktop or mobile
    regex = r"mobile_([A-Za-z0-9+/ ]*)"
    param_string = str(request_param)
    if re.search("mobile", param_string):
        # mobile device name from defined name in config file (ex: mobile_Nexus 5 - Nexus 5)
        browser_type = "MOBILE"
        result = re.search(regex, param_string)
        mobile_device = str(result[1]).rstrip()
        # device:mobile name , browser_type:MOBILE
        return mobile_device, browser_type
    else:
        browser_name = param_string.rstrip().upper()
        browser_type = "DESKTOP"
        return browser_name, browser_type


@pytest.fixture(params=browser_device_list, scope="class")
# Webdriver only called once for all test cases being ran in a class (scope)
def return_driver(request):
    chrome_options = webdriver.ChromeOptions()
    firefox_options = webdriver.FirefoxOptions()

    device_or_browser_name = check_device_list_for_device_type(request.param)

    name, type = device_or_browser_name
    if name == "CHROME":
        if data["BROWSERS"][name]["HEADLESS"]:
            chrome_options.add_argument('--headless')
        if data["BROWSERS"][name]["SCREEN_SIZE"] == "FULLSCREEN":
            chrome_options.add_argument("--start-fullscreen")
            # Additional option ( --start-maximized )	Starts the browser maximized, regardless of any previous settings.
        else:
            # Custom browser size width/height set
            window_size = "window-size={},{}".format(data["BROWSERS"][name]["SCREEN_WIDTH"], data["BROWSERS"][name]["SCREEN_HEIGHT"])
            chrome_options.add_argument(window_size)
        web_driver = webdriver.Chrome(service=Cservice, options=chrome_options)

    if name == "FIREFOX":
        if data["BROWSERS"][name]["HEADLESS"]:
            firefox_options.add_argument('--headless')
        if data["BROWSERS"][name]["SCREEN_SIZE"] == "FULLSCREEN":
            # Additional option --start-maximized 	Starts the browser maximized, regardless of any previous settings.
            web_driver = webdriver.Firefox(service=Fservice, options=firefox_options)
            # Firefox does not currently have a command for full screen, utilize the webdriver
            web_driver.maximize_window()
        else:
            # Custom browser size width/height set
            firefox_options.add_argument("--width={}".format(data["BROWSERS"][name]["SCREEN_WIDTH"]))
            firefox_options.add_argument("--height={}".format(data["BROWSERS"][name]["SCREEN_HEIGHT"]))
            web_driver = webdriver.Firefox(service=Fservice, options=firefox_options)

    # Note: Safari’s WebDriver support for developers is turned off by default
    if name == "SAFARI":
        # Headless option not available for Safari
        if data["BROWSERS"][name]["SCREEN_SIZE"] == "FULLSCREEN":
            # Additional option --start-maximized 	Starts the browser maximized, regardless of any previous settings.
            web_driver = webdriver.Safari(executable_path=safari_path_exe)
            web_driver.maximize_window()
        else:
            # Custom browser size width/height set
            web_driver = webdriver.Safari(executable_path=safari_path_exe)
            web_driver.set_window_size(data["BROWSERS"][name]["SCREEN_WIDTH"], data["BROWSERS"][name]["SCREEN_HEIGHT"])

    if type == "MOBILE":
        mobile_emulation = {"deviceName": name}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        web_driver = webdriver.Chrome(service=Cservice, options=chrome_options)

    request.cls.driver = web_driver
    yield
    web_driver.close()


