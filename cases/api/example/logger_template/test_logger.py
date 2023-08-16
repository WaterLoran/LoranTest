# -*- coding:utf8 -*-
from core.init import *
from core.loran_hook.logger import logger_init, logger_end
from .func_for_logger import for_logger_func_1


class TestLogger(object):

    def setup(self):
        print("__file__", __file__)
        self.logger = logger_init(__file__)
        self.logger.info("这是TestLogger测试用例的setup部分")
        pass

    def test_use_logger(self):
        self.logger.info("这是TestLogger测试用例的过程部分")
        for_logger_func_1()

    def teardown(self):
        logger_end()

