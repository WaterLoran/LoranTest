# 区别于被测环境,这个文件主要记录测试工具的信息,即被用来测试被测系统的测试工具,例如selenium所用到的webdriver等

class Environment(object):
    def __init__(self):
        driver_path = r"E:\代码空间\auto_test_framework\drivers\chromedriver.exe"

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        print("wether need to change another variable")
        self._base_url = value
        print("base_url::set base_url success! ==> {}".format(self._base_url))


