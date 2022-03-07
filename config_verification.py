'''
CONFIG_VERIFICATION SCRIPT CHECKS FOR EXPECTED VALUES SET IN THE CONFIGURATION YAML
EXPECTED BROWSER VERSION AGAINST INSTALLED VERSION,BROWSER HEADLESS OR NOT AND VALID SCREEN SIZE
IF THE VALUE DOES NOT MATCH WHAT IS EXPEXCTED AN ASSERTION IS RAISED AND THE SCRIPT FAILS/ TESTS DO NOT RUN
'''

import subprocess
import re


chrome_regex = "^ChromeDriver\s([0-9.]*)"
firefox_regex = "^geckodriver\s([0-9.]*)"
safari_regex = "Safari\s([0-9.]*)"


def perform_browser_check(browser_key, regex, path_browser, data):
    # Data from the config yaml values
    config_version = data["BROWSERS"][browser_key]["BROWSER_VERSION"]
    # Get the version of browser installed locally
    version_command = '--version'
    output_version = subprocess.check_output([path_browser, version_command])
    browser_version = output_version.decode('utf-8')
    actual_version_re = re.search(regex, browser_version)
    actual_version = actual_version_re[1]
    assert actual_version == config_version, "{} Browser version {} expected version {}".format(browser_key,
                                                                                                actual_version,
                                                                                                config_version)


def check_settings(data):
    # Loops through all browsers and settings once
    # Checks the configuration file for expected locally installed browser version
    # Checks configuration file setting for screen size is either or full screen or custom and width/height > 0
    # Checks if bool type is set for headless setting option (excluding Safari)
    browsers = data["BROWSERS"]

    for browser_key, browser_values in browsers.items():
        # Access the dictionary values for each browser set in the configuration file
        versions_specified = data['BROWSER_EXE_PATHS'][browser_key]

        if browser_key == 'CHROME':
            browser_path = versions_specified
            regex = "^ChromeDriver\s([0-9.]*)"
            perform_browser_check(browser_key, regex, browser_path, data)
        if browser_key == 'FIREFOX':
            browser_path = versions_specified
            regex = "^geckodriver\s([0-9.]*)"
            perform_browser_check(browser_key, regex, browser_path, data)
        if browser_key == 'SAFARI':
            browser_path = versions_specified
            regex = "Safari\s([0-9.]*)"
            perform_browser_check(browser_key, regex, browser_path, data)

        set_screen_size = browser_values['SCREEN_SIZE']
        screen_width = browser_values['SCREEN_WIDTH']
        screen_height = browser_values['SCREEN_HEIGHT']

        if set_screen_size != 'CUSTOM' and set_screen_size != 'FULLSCREEN':
            raise AssertionError(
                '{} Screen size is {} needs to be set to either CUSTOM or FULL'.format(browser_key, set_screen_size))

        elif set_screen_size == 'CUSTOM':
            if screen_width <= 0 or screen_height <= 0:
                raise AssertionError('{} CUSTOM SCREEN_WIDTH and SCREEN_HEIGHT is {},{} and needs to be a number greater than zero'.format(browser_key, screen_width, screen_height))

        if browser_key == 'SAFARI':
            # headless feature not available for Safari browser
            # skip checking Safari browser for headless setting in the configuartion file
            continue

        headless_setting = browser_values['HEADLESS']
        if type(headless_setting) is not bool:
            # Check if the headless value is of type bool
            raise AssertionError(
                "Error {} headless set to {} , needs to be a bool value".format(browser_key, headless_setting))






