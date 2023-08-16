from core.init import *


class TestFunc1Case7:
    def setup_class(self):
        with allure.step('The setup of the class'):
            pass

    def teardown_class(self):
        with allure.step('The teardown of the class'):
            pass

    @allure.suite('接口测试DEMO')
    @allure.epic('')
    @allure.feature('功能1')
    @allure.title("功能1_具体用例7")
    @allure.description('')
    @pytest.mark.medium
    def test_func1_case7(self):
        with allure.step('step1'):
            assert 1 == 1

        logger.info("这里是一条属于  TestFunc1Case7  函数的日志")


