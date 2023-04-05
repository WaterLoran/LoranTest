from selenium import webdriver
from config.selenium_grid import *
from selenium.webdriver import Firefox, Chrome, FirefoxProfile, ChromeOptions


class WebDriver:
    def __init__(self):
        self.web_driver = None
        pass

    def get_web_driver(self):
        # 判断是否需要使用remote的driver
        if use_selenium_grid:
            # TODO 需要对获取不到driver的情况做异常处理
            self.web_driver = webdriver.Remote(
                # selenium_grid_command_executor = 'http://192.168.0.105:4444'
                command_executor=selenium_grid_command_executor,
                options=webdriver.ChromeOptions()
            )
        else:
            # 初始化本地的web_driver
            self._init_chrome()
        return self.web_driver

    def _init_firefox(self):
        profile = FirefoxProfile()
        self.web_driver = Firefox(profile)

    def _init_chrome(self):
        options = ChromeOptions()
        config = dict()
        config['profile.default_content_settings.popups'] = 0
        print("options", options)
        self.web_driver = Chrome(options=options)

