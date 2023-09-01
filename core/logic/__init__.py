import functools
import json
from core.base_api import BaseApi
from core.loran_hook.logger.logger_interface import logger
from core.exception import RuoyiError
from .json_data import JsonData
from .request_data import RequestData
from .response_data import ResponeseData
from .step_data import StepData


class Api:

    def get_fetch(self, **kwargs):
        fetch = None
        if "fetch" in kwargs.keys():
            fetch = kwargs["fetch"]
            del kwargs['fetch']
        logger.info("Api::fetch: " + json.dumps(fetch))
        return fetch, kwargs

    def get_check(self, **kwargs):
        check = None
        if "check" in kwargs.keys():
            check = kwargs["check"]
            del kwargs['check']
        if "CHECK" in kwargs.keys():
            check = kwargs["CHECK"]
            del kwargs['CHECK']
        logger.info("Api::check: " + json.dumps(check))
        return check, kwargs

    def get_api_data(self, api_type, func, **kwargs):
        api_type_field = {
            # "APi的类型" : [[必须存在的字段], [可能存在的字段]]
            "json": [["req_method", "req_url", "req_json"], ["rsp_check", "fill_req_json", "teardown"]],
            "urlencode": [["req_method", "req_url", "req_params"], ["req_json", "rsp_check", "fill_req_params"]],
            "form_data": [["req_method", "req_url"], ["files", "data", "rsp_check"]],
        }
        required_para = api_type_field[api_type][0]
        not_required_para = api_type_field[api_type][1]
        api_data = func(**kwargs)
        if api_data is None:
            logger.error("返回的Api数据是None, 排查思路: 1, 请检查APi数据层是否编写return locals(). "
                         "2, 有可能你定义的是sphere类的logic, 即由多个logic组成的, 该情况不用return,但是该logic不能用api来装饰")
            raise RuoyiError("the_api_data_is_none")

        res_list = []
        # 要求的参数, 必须要有
        for item in required_para:
            try:
                res_list.append(api_data[item])
            except Exception as err:
                raise RuoyiError("api_data_has_no_such_field", item=item)

        # 不要求的参数, 可能会出现
        for item in not_required_para:
            if item in api_data.keys():
                res_list.append(api_data[item])
            else:
                res_list.append(None)
        logger.info(func.__name__ + "::去除fetch和check和的kwargs: " + json.dumps(kwargs))
        return res_list

    def do_check(self, check, func, rsp_data):
        if check:
            logger.info(func.__name__ + "::check: " + json.dumps(check))
            ResponeseData().check_all_expect(rsp_data, check)
        else:
            logger.debug(func.__name__ + "业务脚本层没有定义check信息, 此次请求不做主动断言")
    def do_rsp_check(self, req_json, rsp_data, rsp_check, check):
        rsp_status = "success"
        if rsp_check:  # 如果API数据层定义了断言关系
            rsp_status = ResponeseData().check_rsp_check(req_json, rsp_data, rsp_check, check)
        return rsp_status

    def do_fetch_all_value(self, rsp_data, fetch):
        if fetch:
            fetch_var = ResponeseData().fetch_all_value(rsp_data, fetch)
            logger.info("\n\n\n")
            return fetch_var

    def convert_para(self, func, **kwargs):
        convert_flag = False

        append_kwargs_dict = {}
        wait_to_delete_key = []

        for key, value in kwargs.items():
            logger.debug(f"使用入参中的{key}, {value}去stepData数据中查找数据")
            if key.isupper():
                logger.debug(f"经过判断, 因为{key}是大写的所以要处理")
                convert_key, convert_value = StepData().get_step_data(func, key, value)
                logger.debug(f"转换回来的key, value是{convert_key}, {convert_value}")
                append_kwargs_dict.update({convert_key: convert_value})
                convert_flag = True
                wait_to_delete_key.append(key)

        for key in wait_to_delete_key:
            del kwargs[key]

        if convert_flag:
            kwargs.update(append_kwargs_dict)
            logger.debug("已经对入参做了转换, 转换后的入参数据为" + json.dumps(kwargs, indent=2, ensure_ascii=False))
        return kwargs

    def abstract_api(self, api_type, func, **kwargs):
        logger.info("测试步骤 ==> " + func.__name__)
        logger.info(func.__name__ + "::业务层的kwargs: " + json.dumps(kwargs))

        # 提取fetch入参，并从入参中删除
        fetch, kwargs = Api().get_fetch(**kwargs)

        # 提取check（断言）入参，并从入参中删除
        check, kwargs = Api().get_check(**kwargs)

        # 根据入参去STEP数据中提取映射数据,后转换为实际入参
        kwargs = Api().convert_para(func, **kwargs)

        teardown = None
        # 获取APi数据层的原始数据
        if api_type == "json":
            req_method, req_url, req_json, rsp_check, fill_req_json, teardown = Api().get_api_data("json", func, **kwargs)
            req_data = req_json
        elif api_type == "urlencoded":
            req_method, req_url, req_params, req_json, rsp_check, fill_req_params = Api().get_api_data("urlencode", func, **kwargs)
            req_data = req_params
        elif api_type == "form_data":
            req_method, req_url, files, data, rsp_check = Api().get_api_data("form_data", func, **kwargs)
            req_params = data
        else:
            pass

        # 使用业务层的入参对APi数据层的body进行入参填充
        logger.info(func.__name__ + "步骤的请求")
        if api_type == "json":
            if fill_req_json is not False:
                req_json = RequestData().modify(req_json, **kwargs)
        elif api_type == "urlencoded":
            if fill_req_params is not False:
                req_json = RequestData().modify(req_params, **kwargs)
        else:
            pass

        # 使用请求的基类去做实际请求
        if api_type == "json":
            rsp_data = BaseApi().send(method=req_method, url=req_url, json=req_json)
        elif api_type == "urlencoded":
            if req_json is not None:
                rsp_data = BaseApi().send(method=req_method, url=req_url, params=req_params, json=req_json)
            else:
                rsp_data = BaseApi().send(method=req_method, url=req_url, params=req_params)
        elif api_type == "form_data":
            rsp_data = BaseApi().send(method=req_method, url=req_url, files=files, data=data)
        else:
            pass

        # 根据check入参做断言操作
        logger.info(func.__name__ + " 步骤的断言")
        if api_type == "json" or api_type == "urlencoded" or api_type == "form_data":
            Api().do_check(check, func, rsp_data)

        # 根据Api数据层的预定义关系去做断言
        logger.info(func.__name__ + "步骤的API层预定义数据断言")
        if api_type == "json":
            rsp_status = Api().do_rsp_check(req_json, rsp_data, rsp_check, check)
        elif api_type == "form_data":
            rsp_status = Api().do_rsp_check(data, rsp_data, rsp_check, check)
        elif api_type == "urlencoded":
            rsp_status = Api().do_rsp_check(req_params, rsp_data, rsp_check, check)

        # 根据teardown信息, 去做数据存储
        if teardown:
            if rsp_status == "success":  # 只有响应为成功的时候, 才有获取step信息, 用于恢复环境的作用
                StepData().update_step_data(req_data, rsp_data, teardown)

        # 根据fetch入参提取响应信息
        logger.info(func.__name__ + "步骤的信息提取")
        return Api().do_fetch_all_value(rsp_data, fetch)


    @classmethod
    def json(self, func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            """我是 wrapper 的注释"""
            Api().abstract_api("json", func, **kwargs)
        return wrapper

    @classmethod
    def form_data(self, func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            """我是 wrapper 的注释"""
            Api().abstract_api("form_data", func, **kwargs)
        return wrapper

    @classmethod
    def urlencoded(self, func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            """我是 wrapper 的注释"""
            Api().abstract_api("urlencoded", func, **kwargs)
        return wrapper

    def binary(self, func):
        pass

    def test(self, func):
        pass

    def js(self, func):
        pass

    def html(self, func):
        pass

    def xml(self, func):
        pass
