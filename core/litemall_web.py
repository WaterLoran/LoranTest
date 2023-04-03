from config.environment import Environment
from core.logger.logger_interface import get_logger
from core.base_web_page import WebBasePage
from selenium.webdriver import Firefox, Chrome, FirefoxProfile, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import wraps
import time


class LitemallWeb(WebBasePage):

    def _init_firefox(self):
        profile = FirefoxProfile()
        self.web_driver = Firefox(profile)

    def _init_chrome(self):
        options = ChromeOptions()
        config = dict()
        config['profile.default_content_settings.popups'] = 0
        print("options", options)
        self.web_driver = Chrome(options=options)

    def start(self):
        self._init_chrome()
        self.windows['main'] = self.web_driver.window_handles[-1]

        # 获取 Litemall的环境信息
        env = Environment()
        self.base_url = env.esxi_litemall
        self.logger = get_logger()
        self.logger.info("self.base_url::" + self.base_url)

        self.nav(self.base_url)
        self.maximum()
        return self

    def goto_main_page(self):
        from page.litemall.main_page import MainPage
        return MainPage(self.web_driver)

