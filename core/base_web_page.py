from selenium.webdriver import Firefox, Chrome, FirefoxProfile, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import wraps
import time
from core.logger.logger_interface import get_logger


class WebBasePage:
    def __init__(self, web_driver=None):  # TODO 这里先确定为chrome 后面再改成random
        self.web_driver = web_driver
        self.windows = dict()
        self.logger = get_logger()


    def nav(self, url):
        if self.web_driver:
            self.web_driver.get(url)

    def maximum(self):
        if self.web_driver:
            self.web_driver.maximize_window()

    @property
    def title(self):
        if self.web_driver:
            return self.web_driver.title

    def close(self):
        if self.web_driver:
            self.web_driver.quit()
            self.web_driver = None
            self.windows.clear()

    def open_new_window(self, name):
        self.web_driver.execute_script(f"window.open('about:blank', '{name}')")
        self.windows[name] = self.web_driver.window_handles[-1]

    def switch_to_window(self, name):
        if name not in self.windows:
            return
        self.web_driver.switch_to.window(self.windows[name])

    def close_window(self, name):
        if name not in self.windows:
            return
        self.web_driver.switch_to.window(self.windows[name])
        self.web_driver.close()

    def find(self, by, locator):
        return self.web_driver.find_element(by, locator)

    def find_and_click(self, by, locator):
        self.find(by, locator).click()

    def find_and_send(self, by, locator, text):
        self.find(by, locator).send_keys(text)

    def find_and_gettext(self, by, locator):
        return self.find(by, locator).text

    def screenshot(self, filename):
        self.web_driver.save_screenshot(filename)
        # TODO 这里的截图需要归档到日志目录下

    def get_time(self):
        t = time.localtime(time.time())
        cur_time = time.strftime("%Y-%m-%d_%H_%M_%S", t)
        self.logger.info(cur_time)
        print("当前时间为: {}".format(cur_time))
        return cur_time


