# -*- coding:utf8 -*-
from core.init import *
from core.loran_hook.logger import get_logger


class TestWithCaseInfo(object):

    def setup(self):
        self.logger = get_logger()
        self.logger.info("这里是test_with_case_info用例的setup部分的日志")
        pass

    def test_with_case_info(self):
        self.logger.info("这里是一条属于test_with_case_info函数的日志")
        pass

    def teardown(self):
        self.logger.info("这里是test_with_case_info用例的teardown部分的日志")
        pass
