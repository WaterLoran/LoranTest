from selenium import webdriver
from config.selenium_grid import *
from selenium.webdriver import Firefox, Chrome, FirefoxProfile, ChromeOptions

class SingletonMeta(type):
    """
    功能: 实现一个单例模式的基类,只要子类集成这个类即可实现单例模式
    目的: 解决日志管理器在多处调用都能保证是同一个
    TODO 该单例模式可能存在线程不安全的问题,如果在实际使用中,出现该问题,可重新修改代码,参考连接如下
    https://refactoringguru.cn/design-patterns/singleton/python/example#example-0

    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class WebDriver(metaclass=SingletonMeta):
    def __init__(self):
        self.web_driver = None
        # TODO 后续webdriver的options需要支持在业务脚本层去单独配置
        pass

    def get_web_driver(self):
        if self.web_driver is None:
            return self.create_web_driver()
        else:
            return self.web_driver

    def create_web_driver(self):
        # 判断是否需要使用remote的driver
        if use_selenium_grid:
            # TODO 需要对获取不到driver的情况做异常处理
            self.web_driver = webdriver.Remote(
                # selenium_grid_command_executor = 'http://192.168.0.105:4444'
                command_executor=selenium_grid_command_executor,
                options=webdriver.ChromeOptions()
            )
        else:
            # 初始化本地的web_driver
            self._init_chrome()
        return self.web_driver

    def _init_firefox(self):
        profile = FirefoxProfile()
        self.web_driver = Firefox(profile)

    def _init_chrome(self):
        options = ChromeOptions()
        config = dict()
        config['profile.default_content_settings.popups'] = 0
        print("options", options)
        self.web_driver = Chrome(options=options)

