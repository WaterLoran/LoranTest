from appium import webdriver
from .base_app_page import BasePage


class XueQiuApp(BasePage):
    def start(self):
        if self.driver is None:
            desired_caps = {}
            desired_caps["platformName"] = "Android"
            desired_caps["platformVersion"] = "6.0"
            desired_caps["deviceName"] = ""
            desired_caps["appPackage"] = "com.xueqiu.android"
            desired_caps["appActivity"] = ".view.WelcomeActivityAlias"
            desired_caps["noReset"] = "true"
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            self.driver.implicitly_wait(15)
            pass
        else:
            self.driver.launch_app()
            print("self.driver", self.driver)
        return self

    def restart(self):
        pass

    def stop(self):
        pass

    def goto_main(self):
        from page.xueqiu.main_page import MainPage
        return MainPage(self.driver)

