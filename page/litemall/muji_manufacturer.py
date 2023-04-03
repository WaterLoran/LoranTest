# 此页面封装MUJI制造商的商品的页面
# 备注: 此Page为以游客身份登录litemall的Page
from core.litemall_web import LitemallWeb
from selenium.webdriver.common.by import By
from page.litemall.pillow import Pillow


class MujiManufacturer(LitemallWeb):

    def goto_pillow(self):
        # self.find_and_click(By.XPATH, "//img[contains(@src,\'http://yanxuan.nosdn.127.net/23e0203f1512f33e605f61c28fa03d2d.png\')]")
        self.find_and_click(By.XPATH, "//div[@id=\'app\']/div[2]/div[2]/div/a/img")
        return Pillow(self.web_driver)


