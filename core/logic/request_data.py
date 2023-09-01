import json
from core.loran_hook.logger.logger_interface import logger
from .json_data import JsonData
from core.exception import RuoyiError
import jsonpath

class RequestData(JsonData):

    def __init__(self):
        # self.data = None # 该变量由继承父类而得来
        self.out_data = None

    def set_data(self, json_dict):
        """
        self.data ： 表示用于实际入参填充过程中的数据临时载体
        self.out_data ： 表示针对单个key-value键值对去做入参填充后的数据
        """
        self.data = json_dict
        self.out_data = self.data

    def _edit_one_path(self, paths: list, value):
        """传入一个路径，然后修改他的值"""
        alias_of_data = self.out_data
        for path in paths[0:-1]:
            if path.isdigit():
                alias_of_data = alias_of_data[int(path)]
            else:
                alias_of_data = alias_of_data[path]
        try:
            if paths[-1].isdigit():
                alias_of_data[int(paths[-1])] = value
            else:
                alias_of_data[paths[-1]] = value
        except Exception:
            logger.debug("paths[-1]" + str(paths[-1]))
            logger.debug("alias_of_data" + str(alias_of_data))

    def _modify_single(self, key: str, value):
        if "_" not in key:
            jsonpath_key = "$.." + key
        elif key.startswith("_"):
            jsonpath_key = "$" + key.replace("_", ".")
        else:
            jsonpath_key = "$.." + key.replace("_", ".")

        logger.debug("根据key装换为jsonpath_key后的字符串为" + jsonpath_key)
        paths = self.find_all_values_path_by_jsonpath_key(jsonpath_key)
        logger.debug("根据jsonpath_key获取到的目标所有待修改值得路径为 " + str(paths))
        if isinstance(paths, bool):  # 表示不是数字, 即以为着没找到
            raise RuoyiError("can_not_find_key_in_req_data", key=key)
        if len(paths) > 1:
            raise RuoyiError("req_json_find_too_many_key", key=key, jsonpath_key=jsonpath_key)
        paths = paths[0]  # 因为所获得的路径是二维列表, 需要转换一下
        self._edit_one_path(paths, value)

        return self.out_data

    def modify(self, json_dict, **kwargs):
        out_data = json_dict
        for key, value in kwargs.items():
            self.set_data(out_data)
            out_data = self._modify_single(key, value)
        return out_data
