# 此页面封装MUJI制造商的商品的页面
# 备注: 此Page为以游客身份登录litemall的Page
from core.litemall_web import LitemallWeb
from selenium.webdriver.common.by import By


class Pillow(LitemallWeb):
    def buy_it_now(self):
        self.find_and_click(By.XPATH, "//button[contains(.,\'立即购买\')]")
        pass

