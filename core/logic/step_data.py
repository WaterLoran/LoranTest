import jsonpath
import json

from core.loran_hook.logger.logger_interface import logger
from core.exception import RuoyiError

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


class StepData(metaclass=SingletonMeta):
    def __init__(self):
        self.step = {}
        pass

    def more_action(self, action_type, target_obj):
        if action_type == "to_list":  # 表示需要讲这个对象给变量列表对象, 即
            return [target_obj]
        raise


    def update_step_data(self, req_data, rsp_data, teardown:dict):
        """
        req_data: 请求体的数据, 根据请求类型的不同, json, urlencoded, form_data(请求), 然后
        """
        field_list = ["teardown_func", "para_map", "fetch"]
        for field in field_list:
            if field not in teardown.keys():
                raise  #TODO 需要封装没有该元素的异常
        teardown_func = teardown["teardown_func"]
        para_map = teardown["para_map"]
        fetch = teardown["fetch"]
        origin_para_key = para_map["origin"]
        target_para_key = para_map["target"]

        origin_para_regex = fetch[origin_para_key]
        target_para_content = fetch[target_para_key]
        target_para_more_action = None
        if isinstance(target_para_content, str):  # 如果他是字符串, 那么就默认是jsonpath_regex的字符串了
            target_para_regex = target_para_content
        elif isinstance(target_para_content, list):
            target_para_regex = target_para_content[0]
            target_para_more_action = target_para_content[1]

        logger.debug(json.dumps(req_data, indent=2, ensure_ascii=False))
        logger.debug(json.dumps(rsp_data, indent=2, ensure_ascii=False))
        logger.debug(f"将使用{origin_para_regex}表达式去请求数据中提取信息")
        logger.debug(f"将使用{target_para_regex}表达式去响应数据中提取信息")
        if len(jsonpath.jsonpath(req_data, origin_para_regex)) != 1:
            logger.error(f"请确认API数据层所定义的从请求数据中获取数据的jsonpathregex表达式")
            raise
        if len(jsonpath.jsonpath(rsp_data, target_para_regex)) != 1:
            logger.error(f"请确认API数据层所定义的从响应数据中获取数据的jsonpathregex表达式, 以及确认一下,请求是否成功")
            raise
        origin_para_value = jsonpath.jsonpath(req_data, origin_para_regex)[0]
        target_para_value = jsonpath.jsonpath(rsp_data, target_para_regex)[0]
        if target_para_more_action:  # 如果他有其他要求的操作, 那么就做这个操作
            target_para_value = StepData().more_action(target_para_more_action, target_para_value)


        if isinstance(teardown_func, str):
            teardown_func_list = [teardown_func]
        else:
            teardown_func_list = teardown_func

        for each_func in teardown_func_list:
            each_step = {
                each_func: {
                    origin_para_key: origin_para_value,
                    target_para_key: target_para_value,
                }
            }
            if each_func not in self.step.keys():
                self.step.update({each_func: []})
            self.step[each_func].append(each_step[each_func])

        # logger.info("StepData的信息" + json.dumps(self.step, indent=2, ensure_ascii=False))
        pass

    def get_step_data(self, func, key_input:str, value_input):
        get_convert_data_flag = False
        logger.debug("self.step" + json.dumps(self.step, indent=2, ensure_ascii=False))
        logger.debug("函数名称为" + str(func.__name__))
        func_data_list = self.step[str(func.__name__)]  # 这里的func_name 是一个对象, 需要先转换为字符串
        logger.debug("func_data_list" + str(func_data_list))
        logger.debug(f"key_input, value_input信息为{key_input}, {value_input}")
        for each_data in func_data_list:
            for t_key, t_value in each_data.items():
                if t_key == key_input.lower() and t_value == value_input:  # 这里输入的key是大写的, 需要转换一下
                    get_convert_data_flag = True
                    continue  # 如果这对key-value匹配上了, 那就不更新下面的new_key, new_value的数据
                new_key = t_key
                new_value = t_value
            if get_convert_data_flag:
                logger.debug(f"返回的数据new_key, new_value, {new_key}, {new_value}")
                return new_key, new_value

