from core.xueqiu_app import XueQiuApp
from appium.webdriver.common.appiumby import AppiumBy
from .search_page import SearchPage
import time

class MainPage(XueQiuApp):
    _SEARCH_BOX_ELEMENT = (AppiumBy.ID, "com.xueqiu.android:id/tv_search")

    def click_search(self):
        print("22self.driver", self.driver)
        self.find_and_click(AppiumBy.ID, "com.xueqiu.android:id/post_status")

        time.sleep(1)
        self.find_and_click(*self._SEARCH_BOX_ELEMENT)

        return SearchPage(self.driver)
