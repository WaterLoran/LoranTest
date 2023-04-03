# -*- coding:utf8 -*-
import time
from core.logger import get_logger
from core.litemall_web import LitemallWeb

class TestWithCaseInfo(object):

    def setup(self):
        self.logger = get_logger()
        self.logger.info("这里是test_with_case_info用例的setup部分的日志")
        pass

    def test_with_case_info(self):
        self.logger.info("这里是一条属于test_with_case_info函数的日志")
        litemall = LitemallWeb()
        time.sleep(3)
        main_page = litemall.start().goto_main_page()
        time.sleep(3)
        muji_manufacturer = main_page.goto_muji_manufacturer()
        time.sleep(3)
        pillow = muji_manufacturer.goto_pillow()
        time.sleep(3)
        pillow.buy_it_now()
        time.sleep(3)  # 用于观察现象
        pass

    def teardown(self):
        self.logger.info("这里是test_with_case_info用例的teardown部分的日志")
        pass
