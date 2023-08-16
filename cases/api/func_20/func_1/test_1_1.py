from core.init import *
# from common.ruoyi_logic import *


class TestFunc1Case1:
    def setup_class(self):
        with allure.step('The setup of the class'):
            pass

    def teardown_class(self):
        with allure.step('The teardown of the class'):
            pass

    @allure.suite('接口测试DEMO')
    @allure.epic('')
    @allure.feature('功能1')
    @allure.title("功能1_具体用例1")
    @allure.description('')
    @pytest.mark.medium
    def test_func1_case1(self):
        with allure.step('step1'):
            assert 1 == 1

        logger.debug("这里是一条属于  TestFunc1Case1   函数的日志  DEBUG  ")
        logger.info("这里是一条属于  TestFunc1Case1  函数的日志  INFO")
        logger.warning("这里是一条属于  TestFunc1Case1  函数的日志  WARNING")
        logger.error("这里是一条属于  TestFunc1Case1  函数的日志  ERROR")

