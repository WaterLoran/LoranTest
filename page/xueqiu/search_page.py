from appium.webdriver.common.appiumby import AppiumBy
from core.xueqiu_app import XueQiuApp
from .search_result_page import SearchResultPage


class SearchPage(XueQiuApp):
    def input_searchcontent(self, search_key):
        self.find_and_send(AppiumBy.ID, "com.xueqiu.android:id/search_input_text", search_key)
        return self

    def click_searchresult(self, text):
        self.find_and_click(AppiumBy.XPATH, f"//*[@text='{text}']")
        print("cleck search result::self.driver", self.driver)
        return SearchResultPage(self.driver)
