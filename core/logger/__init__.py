# -*- coding:utf8 -*-
import logging
import logging.handlers
import os
import time
from config.frame.basic import LOG_PATH


class LoggerManager:
    def __init__(self):
        # 用于记录logger的配置信息
        self.logger_info = dict()
        self.user_handler = None
        self.default_logger_name = "main"  # 因为pytest串行执行时,只有一个进程线程,脚本执行前后需要注册解注册日志,多线程执行时,线程间独立

    def get_log_file_name(self, case_file_path):
        new_folder_list = []
        py_file_name = os.path.split(case_file_path)[1]
        py_file_name = py_file_name.strip(".py")
        current = time.localtime()
        log_file_name = py_file_name + "_%d_%d_%d_%d_%d_%d" % (
            current.tm_year, current.tm_mon, current.tm_mday,
            current.tm_hour, current.tm_min, current.tm_sec
        ) + ".log"

        new_folder_list.append(py_file_name.strip(".py"))

        file_path = os.path.split(case_file_path)[0]
        cur_folder = ""
        while cur_folder != "cases":
            path_detail = os.path.split(file_path)
            file_path = path_detail[0]
            cur_folder = path_detail[1]
            new_folder_list.append(cur_folder)
        new_folder_list = new_folder_list[::-1]

        t_folder = "cases"
        for i in range(1, len(new_folder_list)):
            t_folder = os.path.join(t_folder, new_folder_list[i])

        log_file_path = os.path.join(t_folder, log_file_name)
        log_file_path = os.path.join(LOG_PATH, log_file_path)

        print("get_log_file_name::所要输出日志文件的路径=>log_file_path", log_file_path)

        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))
        file = open(log_file_path, 'w')
        file.close()
        return log_file_path

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
        """

        print("filename", case_file_path)
        filename = self.get_log_file_name(case_file_path)

        log_format = kwargs.get("format", None)
        if log_format is None:
            log_format = "%(asctime)s %(filename)s::%(module)s::%(funcName)s[%(lineno)d] %(levelname)s: %(message)s"

        # 获取新的loger实例
        logger_name = self.default_logger_name
        logger = logging.getLogger(logger_name)

        self.logger_info[logger_name] = dict()
        self.logger_info[logger_name]["timestamp"] = time.localtime()

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
            stream_handler.setFormatter(logging.Formatter(fmt=log_format))
            logger.addHandler(stream_handler)

        logger.setLevel(default_level)
        self.logger_info[logger_name]['logger'] = logger

        return logger

    def unregister(self, logger_name="main"):
        """
        删除注册的logger, 同时将需要打包的logger文件打包
        :param logger_name:
        :return:
        """
        print("logging.Logger.manager.loggerDict", logging.Logger.manager.loggerDict)
        print("logger_info", self.logger_info)
        if logger_name in logging.Logger.manager.loggerDict:
            logging.Logger.manager.loggerDict.pop(logger_name)
            # self.logger_info.pop(logger_name) # 因为如果在不同的地方初始化,那么这个信息并非是共享的,所以展示删除这行代码

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

