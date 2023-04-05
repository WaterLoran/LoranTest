from config.environment import Environment
from core.logger.logger_interface import get_logger
from core.base_web_page import WebBasePage
from core.web_drive import WebDriver

class LitemallWeb(WebBasePage):

    def start(self):
        self.web_driver = WebDriver().get_web_driver()
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

    def quit(self):
        self.web_driver.quit()


