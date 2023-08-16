import os
import time
from core.loran_hook.logger.logger_interface import get_logger
from core.loran_hook.logger import get_ui_screecshot_directory
from .web_driver import WebDriver
from config.environment import Environment
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

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


class WebBasePage(metaclass=SingletonMeta):
    def __init__(self):  # TODO 这里先确定为chrome 后面再改成random
        self._driver = WebDriver().get_web_driver()
        self.windows = dict()
        self._logger = get_logger()
        self.first_login()


    def first_login(self):
        self._login_page_flag = False
        if self._login_page_flag is False:
            self._do_login()
            self._login_page_flag = True

    def nav(self, url):
        if self._driver:
            self._driver.get(url)

    def maximum(self):
        if self._driver:
            self._driver.maximize_window()

    @property
    def title(self):
        if self._driver:
            return self._driver.title

    def close(self):
        if self._driver:
            self._driver.quit()
            self._driver = None
            self.windows.clear()

    def open_new_window(self, name):
        self._driver.execute_script(f"window.open('about:blank', '{name}')")
        self.windows[name] = self._driver.window_handles[-1]

    def switch_to_window(self, name):
        if name not in self.windows:
            return
        self._driver.switch_to.window(self.windows[name])

    def close_window(self, name):
        if name not in self.windows:
            return
        self._driver.switch_to.window(self.windows[name])
        self._driver.close()

    def find(self, by, locator):
        # self.screenshot()  # TODO 这里需要适配截图的代码
        # 显示等待该元素可以被定位
        # locator_tuple = (by, locator)
        # WebDriverWait(self._driver, 5).until(expected_conditions.presence_of_element_located(locator_tuple))
        time.sleep(0.5)
        return self._driver.find_element(by, locator)

    def _do_login(self):
        url = Environment().base_url + "webapp/login"
        self._driver.get(url)
        self._driver.maximize_window()
        self._driver.find_element(By.ID, "basic_username").click()
        self._driver.find_element(By.ID, "basic_username").send_keys("admin")
        self._driver.find_element(By.ID, "basic_password").send_keys("admin123")
        self._driver.find_element(By.CSS_SELECTOR, ".sc-d5cbc0cb-2").click()
        self._driver.execute_script("window.scrollTo(0,0)")

    def find_and_click(self, by, locator):
        self.find(by, locator).click()

    def find_and_send(self, by, locator, text):
        self.find(by, locator).send_keys(text)

    def find_and_send_then_enter(self, by, locator, text):
        self.find(by, locator).send_keys(text, Keys.ENTER)


    def find_and_drag_to_buttom(self, by, locator):
        # TODO 未实现成功, 待调试
        element = self.find(by, locator)

        action = ActionChains(self._driver)
        time.sleep(1)
        action.move_to_element(element)
        time.sleep(1)
        action.click_and_hold(element)
        time.sleep(1)
        action.move_by_offset(0, 600)
        action.release()
        # 执行动作
        action.perform()

    def find_and_move_here(self, by, locator):
        time.sleep(2)
        element = self.find(by, locator)

        action = ActionChains(self._driver)
        action.move_to_element(element)
        action.perform()

    def find_and_gettext(self, by, locator):
        return self.find(by, locator).text

    def screenshot(self):
        directory = get_ui_screecshot_directory()
        if not os.path.exists(directory):
            os.makedirs(directory)
        time_suffix_jpg = str(int(time.time())) + ".jpg"
        jpg_path = os.path.join(directory, time_suffix_jpg)
        self._driver.save_screenshot(jpg_path)

    def get_time(self):
        t = time.localtime(time.time())
        cur_time = time.strftime("%Y-%m-%d_%H_%M_%S", t)
        self._logger.info(cur_time)
        print("当前时间为: {}".format(cur_time))
        return cur_time
