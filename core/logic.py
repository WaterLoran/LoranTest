import jsonpath
import functools
import json
from core.base_api import BaseApi
from core.logger.logger_interface import logger


class RequestData:
    class KeyError(Exception):
        def __init__(self, error_key):
            error_dict = {
                "find_too_many_key": "The key value is incorrect. The request data contains at least two keys named $key. "
                                     "Please modify the incoming key name, that is, $parent key + $key",
                "can_not_find_key": "The key you entered could not be found in the dictionary",
            }
            self.error_info = error_dict[error_key]

        def __str__(self):
            return repr(self.error_info)

    class FindKeyError(Exception):
        def __str__(self):
            return repr("The key you entered could not be found in the dictionary")

    def __init__(self):
        self.data = None
        self.out_data = None

    def set_data(self, json_dict):
        self.data = json_dict
        self.out_data = self.data

    def iter_node(self, rows, road_step, target):
        if isinstance(rows, dict):
            key_value_iter = (x for x in rows.items())
        elif isinstance(rows, list):
            key_value_iter = (x for x in enumerate(rows))
        else:
            return
        for key, value in key_value_iter:
            current_path = road_step.copy()
            current_path.append(key)
            if key == target:
                yield current_path
            if isinstance(value, (dict, list)):
                yield from self.iter_node(value, current_path, target)

    def find_one(self, key: str) -> list:
        path_iter = self.iter_node(self.data, [], key)
        for path in path_iter:
            return path
        return []

    def find_all(self, key: str) -> list:
        path_iter = self.iter_node(self.data, [], key)
        return list(path_iter)

    def _edit_one_path(self, paths: list, value):
        alias_of_data = self.out_data
        for path in paths[0:-1]:
            alias_of_data = alias_of_data[path]
        alias_of_data[paths[-1]] = value

    def change(self, key: str, value):
        if "_" not in key:
            res = self.find_all(key)
            if len(res) > 1:
                raise self.KeyError("find_too_many_key")
            paths = res[0]
            self._edit_one_path(paths, value)
        else:
            key_list = key.split("_")
            res = self.find_all(key_list[-1])
            for temp in key_list:
                if temp not in res[0]:
                    raise self.KeyError("can_not_find_key")
            paths = res[0]
            self._edit_one_path(paths, value)
            pass

        return self.out_data

    def modify(self, json_dict, **kwargs):
        out_data = json_dict
        for key, value in kwargs.items():
            self.set_data(out_data)
            out_data = self.change(key, value)
        return out_data


class ResponeseData:

    def fetch_one_value(self, data, var_info):
        var_name = var_info[0]
        json_path_reg = var_info[1]
        value = jsonpath.jsonpath(data, json_path_reg)[0]
        return value

    def fetch_all_value(self, data, fetch_info):
        # TODO 这里有可能存在一个问题,只对单个调教的信息提取做处理,未对多条件的进行处理
        for info in fetch_info:
            return self.fetch_one_value(data, info)


class Api:
    @classmethod
    def json(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """我是 wrapper 的注释"""
            # 提取fetch入参
            fetch = None
            if "fetch" in kwargs.keys():
                fetch = kwargs["fetch"]
                del kwargs['fetch']

            res = func(*args, **kwargs)
            logger.debug(func.__name__ + "::kwargs: " + json.dumps(kwargs))

            req_method, url, body_data = res
            req_body = RequestData().modify(body_data, **kwargs)
            logger.debug(func.__name__ + "::req_body: " + json.dumps(req_body))

            req_api = BaseApi(role="admin")
            rsp_data = req_api.send(method=req_method, url=url, json=req_body)
            logger.debug(func.__name__ + "::req_body: " + json.dumps(rsp_data))

            # 针对fetch入参做处理
            if fetch:
                fetch_var = ResponeseData().fetch_all_value(rsp_data, fetch)
                logger.debug(func.__name__ + "::req_body: " + json.dumps(fetch_var))
        return wrapper

    def form(self):
        pass

    def urlencoded(self):
        pass

    def binary(self):
        pass

    def test(self):
        pass

    def js(self):
        pass

    def html(self):
        pass

    def xml(self):
        pass




