from core.logger.logger_interface import logger
from functools import wraps
from threading import Thread
import time


class Event:
    @classmethod
    def loop(cls, times):
        """
        被该装饰器装饰的函数,将会在未抛出异常的情况下,串行循环执行times次
        :param times: 所要执行的事情的次数
        :return:
        """
        logger.info("正在调用Event.loop,在未抛异常的情况下,将会串行循环执行目标事件{}次".format(times))

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(times):
                    func(*args, **kwargs)
            return wrapper
        return decorate

    @classmethod
    def loop_to_success(cls, times):
        """
        被该装饰器装饰的函数,将会在未抛出异常的情况下,串行循环执行times次
        :param times: 所要执行的事情的次数
        :return:
        """
        logger.info("正在调用Event.loop,在未抛异常的情况下,将会串行循环执行目标事件{}次".format(times))

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                success_flag = False
                for i in range(times):
                    try:
                        func(*args, **kwargs)
                        success_flag = True
                    except Exception as err:
                        logger.info("正在调用Event.force,抛出异常,err为{}".format(err))
                    if success_flag:
                        break
            return wrapper
        return decorate

    @classmethod
    def force(cls, times):
        """
        被该装饰器装饰的函数,将会在未抛出异常的情况下,串行循环执行times次
        :param times: 所要执行的事情的次数
        :return:
        """
        logger.info("正在调用Event.force,不管是否抛出异常,都会会串行循环执行目标事件{}次".format(times))

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(times):
                    try:
                        func(*args, **kwargs)
                    except Exception as err:
                        logger.info("正在调用Event.force,抛出异常,err为{}".format(err))
            return wrapper
        return decorate

    @classmethod
    def background(cls, times, delay=0.01):
        """
        被该装饰器装饰的函数将以多线程的方式执行times次,并且每两次操作之间间隔delay秒
        :param delay: 事件执行的事件间隔
        :param times: 所要执行的事情的次数
        :return:
        """
        # logger.info("正在调用Event.force,不管是否抛出异常,都会会串行循环执行目标事件{}次".format())

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                def bg_func():
                    for i in range(times):
                        func(*args, **kwargs)
                        time.sleep(delay)
                t = Thread(target=bg_func)
                t.start()
            return wrapper

        return decorate


if __name__ == "__main__":
    @Event.loop_to_success(5)
    def print_hello():
        print("999")

    @Event.loop(50)
    def print_loop():
        print("print_loop")
        time.sleep(1)

    @Event.force(50)
    def print_force():
        print("print_force\n")
        time.sleep(1)

    @Event.background(100, 1)
    def print_background_info():
        print("print_background_info\n")


    print_background_info()
    print_force()

