import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MockappSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_mockapp(self):
        driver = self.driver
        driver.get("http://demo-mockapp.jx-staging.flugel.it/")
        self.assertIn("Registered", driver.title)
        time.sleep(5)
        elem = driver.find_element_by_css_selector(".btn-default")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

