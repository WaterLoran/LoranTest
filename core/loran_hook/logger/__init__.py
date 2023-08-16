# -*- coding:utf8 -*-
import logging
import logging.handlers
import os
import time
import colorlog
from ..path import LOG_PATH
from .allure_logger import AllureLogger

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

class LoggerManager(metaclass=SingletonMeta):
    def __init__(self):
        # 用于记录logger的配置信息
        self.logger_info = dict()
        self.user_handler = None
        self.default_logger_name = "main"  # 因为pytest串行执行时,只有一个进程线程,脚本执行前后需要注册解注册日志,多线程执行时,线程间独立

    def get_log_file_name(self, case_file_path):
        print("case_file_path", case_file_path)
        new_folder_list = []
        py_file_name = os.path.split(case_file_path)[1]
        py_file_name = py_file_name.strip(".py")
        print("py_file_name", py_file_name)

        # 获取时间戳后缀
        current = time.localtime()
        time_suffix = "_%d_%d_%d_%d_%d_%d" % (
            current.tm_year, current.tm_mon, current.tm_mday,
            current.tm_hour, current.tm_min, current.tm_sec
        )
        print("time_suffix", time_suffix)

        # 根据用例文件获取相对路径信息
        new_folder_list.append(py_file_name.strip(".py"))
        file_path = os.path.split(case_file_path)[0]

        print("file_path", file_path)

        cur_folder = ""
        while cur_folder != "cases":
            path_detail = os.path.split(file_path)
            file_path = path_detail[0]
            cur_folder = path_detail[1]
            new_folder_list.append(cur_folder)
        new_folder_list = new_folder_list[::-1]

        print("new_folder_list", new_folder_list)

        t_folder = "cases"  # 用例文件的相对路径, 即根据用例的相对路径,去记录一些路径信息,将用于生存路径
        for i in range(1, len(new_folder_list)):
            t_folder = os.path.join(t_folder, new_folder_list[i])

        # 生成日志文件所在的目录(绝对)
        # print("BASE_PATH", BASE_PATH)
        # print("LOG_PATH", LOG_PATH)
        log_file_directory = os.path.join(LOG_PATH, t_folder)  # 日志所在的绝对目录

        print("log_file_directory", log_file_directory)

        # 获取日志文件的文件名, 名字在中包含日志时间戳
        log_file_name = py_file_name + time_suffix + ".log"
        log_file_path = os.path.join(log_file_directory, log_file_name)
        print("LoggerManager::get_log_file_name::get_log_file_name::所要输出日志文件的路径=>log_file_path", log_file_path)

        # 根据日志文件的绝对路径,去创建出所在的目录,否则写文件的时候,会失败
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))
        file = open(log_file_path, 'w')
        file.close()

        # 获取UI_自动化测试时需要保存截图文件的目录
        ui_directory = log_file_name.strip(".log")  # 保存截图文件的目录名字和日志文件的命名一样
        ui_screenshot_path = os.path.join(log_file_directory, ui_directory)
        return log_file_path, ui_screenshot_path

    def get_screenshot_file_path(self):
        # 需要重构下上面的代码,共用获取通用信息部分
        pass

    def register(self, case_file_path, console=True, default_level=logging.DEBUG, **kwargs):
        """
        注册logger
        :param logger_name:
        :param file_name:
        :param console:
        :param default_level:
        :param kwargs:
        :return:
        """
        """ 
        logger_info[logger_name] = dict(), 其中的key分别表示
        timestamp: 表示创建的时间戳
        file_path: 表示日志存储的路径
        logger: 表示日志器
        thread: 表示所属的线程
        ui_directory: 表示UI截图信息所在的目录
        """
        filename, ui_screenshot_path = self.get_log_file_name(case_file_path)

        # 设置不同级别的日志在终端中显示的颜色
        log_colors_config = {
            'DEBUG': 'white',  # cyan white
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        log_format = kwargs.get("format", None)
        if log_format is None:
            log_format = "%(asctime)s %(filename)s::%(module)s::%(funcName)s[%(lineno)d] %(levelname)s: %(message)s"

        # 获取新的loger实例
        logger_name = self.default_logger_name
        # logging.setLoggerClass(AllureLogger)
        logger = logging.getLogger(logger_name)

        self.logger_info[logger_name] = dict()
        self.logger_info[logger_name]["timestamp"] = time.localtime()
        self.logger_info[logger_name]["ui_directory"] = ui_screenshot_path

        # 如果设置了file_count, 则默认一个文件大小为1MB
        file_size_limit = kwargs.get("size_limit", 10*1024*1024)  # 即一个日志文件最大10M
        file_max = kwargs.get("file_max", 6)
        file_mode = kwargs.get("mode", "w")

        if filename:
            self.logger_info[logger_name]["file_path"] = os.path.dirname(filename)
            file_handler = logging.handlers.RotatingFileHandler(
                filename=filename,
                mode=file_mode,
                maxBytes=file_size_limit,
                backupCount=file_max,
                encoding='utf-8'
            )
            file_handler.setFormatter(logging.Formatter(fmt=log_format))
            self.user_handler = file_handler
            logger.addHandler(file_handler)

        if console:
            stream_handler = logging.StreamHandler()
            console_formatter = colorlog.ColoredFormatter(
                fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
                log_colors=log_colors_config
            )
            stream_handler.setFormatter(console_formatter)
            logger.addHandler(stream_handler)

        logger.setLevel(default_level)  #  设置打印日志的级别, 假设这里的default_level是debug, 就相当于, info, warning, error
        self.logger_info[logger_name]['logger'] = logger
        self.logger_info[logger_name]['file_handler'] = file_handler
        self.logger_info[logger_name]['stream_handler'] = stream_handler

        return logger

    def unregister(self, logger_name="main"):
        """
        删除注册的logger, 同时将需要打包的logger文件打包
        :param logger_name:
        :return:
        """
        if logger_name in logging.Logger.manager.loggerDict:
            logging.Logger.manager.loggerDict.pop(logger_name)
            logger = self.get_logger(logger_name="main")
            # 把日志器的句柄移除, 如果不移除, 就会一直打印日志在之前的文件中
            logger.removeHandler(self.logger_info[logger_name]['file_handler'])
            logger.removeHandler(self.logger_info[logger_name]['stream_handler'])
            self.logger_info.pop(logger_name)  # 删除用户的备份信息

    def get_logger(self, logger_name="main"):
        return logging.getLogger(logger_name)  # 因为有可能在多次初始化,日志管理器的类,所以先暂时直接返回
        # if logger_name in self.logger_info:
        #     return self.logger_info[logger_name]["logger"]
        # raise NameError(f"No log names {logger_name}")


def logger_init(case_file_path):
    logger_mgt = LoggerManager()
    logger = logger_mgt.register(case_file_path)
    return logger

def get_logger():
    logger_mgt = LoggerManager()
    logger = logger_mgt.get_logger()
    return logger

def logger_end():
    logger_mgt = LoggerManager()
    logger_mgt.unregister()

def get_ui_screecshot_directory():
    logger_mgt = LoggerManager()
    logger_name = logger_mgt.default_logger_name
    return logger_mgt.logger_info[logger_name]["ui_directory"]

def logger_unregister(logger):
    for handler in logger.handlers:
        logger.removeHandler(handler)

