'''
TESTS WRITTEN FOR THE CARNEGIE HOMEPAGE
'''

from pages.homepage import Homepage
from base_file import BasicTest


class TestPage(BasicTest):
    # Inherit BasicTest class fixture to access the web driver
    # Taking screenshots after a test step example: driver.save_screenshot(‘/Screenshots/foo.png’)

    def test_check_for_carnegie_logo(self):
        # call methods w/ locators from the page
        self.hp = Homepage(self.driver)
        self.hp.check_hp_compnay_logo()

    def test_check_technology_dropdown_elements(self):
        hp = Homepage(self.driver)
        hp.hover_over_top_technologies()
        hp.check_if_technology_drop_active()
        hp.check_for_nav_bar_technologies_link_text_options()

    def test_check_company_dropdown_elements(self):
        hp = Homepage(self.driver)
        hp.hover_over_top_company()
        hp.check_if_company_drop_active()
        hp.check_for_nav_bar_company_link_text_options()

    def test_check_for_contact_element(self):
        self.hp = Homepage(self.driver)
        self.hp.check_for_nav_contact_text()

    def test_check_mission_element(self):
        self.hp = Homepage(self.driver)
        self.hp.check_mission_statement()

    # use verify to check for manual test cases that need to be ran
    # def check_promo(self):
    #     self.verify("Can you find the moon?")
