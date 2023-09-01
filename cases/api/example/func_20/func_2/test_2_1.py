from core.init import *



class TestFunc2Case1:
    def setup_class(self):
        with allure.step('The setup of the class'):
            pass

    def teardown_class(self):
        with allure.step('The teardown of the class'):
            pass

    @allure.suite('接口测试DEMO')
    @allure.epic('')
    @allure.feature('功能2')
    @allure.title("功能2_具体用例1")
    @allure.description('')
    @pytest.mark.medium
    def test_func2_case1(self):
        with allure.step('step1'):
            assert 1 == 1

        logger.info("这里是一条属于  TestFunc1Case1  函数的日志")
