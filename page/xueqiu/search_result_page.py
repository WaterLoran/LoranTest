from appium.webdriver.common.appiumby import AppiumBy
from core.xueqiu_app import XueQiuApp


class SearchResultPage(XueQiuApp):
    def goto_stock_tab(self):
        self.find_and_click(AppiumBy.XPATH, "//*[@text='股票']")
        return self

    def get_price(self):
        current_price = self.find_and_gettext(AppiumBy.XPATH,
                        "//*[@text='BABA']/../../..//*[@resource-id='com.xueqiu.android:id/current_price']")
        return float(current_price)


