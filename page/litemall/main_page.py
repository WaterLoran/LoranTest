# 备注: 此Page为以游客身份登录litemall的Page
from core.litemall_web import LitemallWeb
from selenium.webdriver.common.by import By
from page.litemall.muji_manufacturer import MujiManufacturer

class MainPage(LitemallWeb):

    def goto_muji_manufacturer(self):
        self.find_and_click(By.XPATH, "//img[contains(@src,\'http://yanxuan.nosdn.127.net/1541445967645114dd75f6b0edc4762d.png\')]")
        # self.find_and_click(By.XPATH, "//div[@id=\'app\']/div[2]/div[6]/div[2]/div/div/div/img")
        return MujiManufacturer(self.web_driver)


    def goto_new_product_launch(self):
        pass