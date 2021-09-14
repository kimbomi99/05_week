from selenium import webdriver
import unittest

class FuntionalTest(unittest.TestCase):
    def setUp(self):
        path = "./chromedriver"
        self.driver = webdriver.Chrome(path)

    def tearDown(self):
        self.driver.quit()

    def test_has_worked_in_title(self):
        self.driver.get("http://localhost:8000")
        self.assertIn("worked", self.driver.title)

    def test_has_install_in_title(self):
        self.driver.get("http://localhost:8000")
        self.assertIn("install", self.driver.title)