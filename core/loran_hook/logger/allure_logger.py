import logging
import sys

import allure
from selenium.webdriver.remote.webdriver import WebDriver



class AllureLogger(logging.Logger):
    formatter = None

    def __init__(self, name):
        super().__init__(name)
        self.formatter = logging.Formatter(fmt='%(asctime)s-%(levelname)s:\t %(message)s',
                                           datefmt='%H:%M:%S')

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1,
             driver: WebDriver = False):
        """
                Low-level logging routine which creates a LogRecord and then calls
                all the handlers of this logger to handle the record.
                """
        sinfo = None
        if logging._srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                 None, func, None, None)
        title = self.formatter.format(record)
        with allure.step(title):#输出step
            # if driver:#如果参数中有webDriver对象则进行截屏
            #     basic.save_capture(driver, "快照")
            #     pass
            if exc_info:
                if isinstance(exc_info, BaseException):
                    exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
                elif not isinstance(exc_info, tuple):
                    exc_info = sys.exc_info()
            record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                     exc_info, func, extra, sinfo)
            if exc_info:#如果执行异常，把堆栈信息写入allure attach文件
                allure.attach(self.formatter.format(record), "堆栈", allure.attachment_type.TEXT)
                pass
            self.handle(record)
            pass
        pass

    pass
