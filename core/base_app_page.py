import time
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver = None):
        self.driver = driver

    def find(self, by, locator):
        return self.driver.find_element(by, locator)

    def find_and_click(self, by, locator):
        self.find(by, locator).click()

    def find_and_send(self, by, locator, text):
        self.find(by, locator).send_keys(text)

    def find_and_gettext(self, by, locator):
        return self.find(by, locator).text

    def screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def get_time(self):
        t = time.localtime(time.time())
        cur_time = time.strftime("%Y-%m-%d_%H_%M_%S", t)
        print("当前时间为: {}".format(cur_time))
        return cur_time
