import os
import time
from core.logger.logger_interface import get_logger
from core.logger import get_ui_screecshot_directory


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
        self.screenshot()
        return self.web_driver.find_element(by, locator)

    def find_and_click(self, by, locator):
        self.find(by, locator).click()

    def find_and_send(self, by, locator, text):
        self.find(by, locator).send_keys(text)

    def find_and_gettext(self, by, locator):
        return self.find(by, locator).text

    def screenshot(self):
        directory = get_ui_screecshot_directory()
        if not os.path.exists(directory):
            os.makedirs(directory)
        time_suffix_jpg = str(int(time.time())) + ".jpg"
        jpg_path = os.path.join(directory, time_suffix_jpg)
        self.web_driver.save_screenshot(jpg_path)


    def get_time(self):
        t = time.localtime(time.time())
        cur_time = time.strftime("%Y-%m-%d_%H_%M_%S", t)
        self.logger.info(cur_time)
        print("当前时间为: {}".format(cur_time))
        return cur_time


