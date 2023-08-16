import jsonpath

from core.loran_hook.logger.logger_interface import logger
from core.exception import RuoyiError

class JsonData:

    class KeyError(Exception):
        def __init__(self, error_key, **kwargs):

            if len(kwargs) == 0:
                error_dict = {
                    "find_too_many_key": "The key value is incorrect. The request data contains at least two keys named $key. "
                                         "Please modify the incoming key name, that is, $parent key + $key",
                    "can_not_find_key": "The key you entered could not be found in the dictionary",
                }
            else:
                error_dict = {
                    "find_too_many_key": "The key value is incorrect. The request data contains at least two keys named $key. "
                                         "Please modify the incoming key name, that is, $parent key + $key, 关键信息为{}".format(str(kwargs["key_info"])),
                    "can_not_find_key": "The key you entered could not be found in the dictionary, 关键信息为{}".format(str(kwargs["key_info"])),
                }
            self.error_info = error_dict[error_key]

        def __str__(self):
            return repr(self.error_info)

    class FindKeyError(Exception):
        def __str__(self):
            return repr("The key you entered could not be found in the dictionary")

    data = None

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

    def find_all_values_path_by_key(self, key: str) -> list:
        """
        传入一个key，然后对json中的所有信息进行查找，如果有匹配的key，则返回他的路径，比如[["a", "b", "c", "d"]]
        如果匹配到多个key，则返回的数据可能为[["a1", "b", "c", "d"]， ["a2", "b", "c", "d"]]
        """
        path_iter = self.iter_node(self.data, [], key)
        return list(path_iter)

    def find_all_values_path_by_jsonpath_key(self, jsonpath_key: str) -> list:
        result = jsonpath.jsonpath(self.data, jsonpath_key, result_type="IPATH")
        return result

    def get_value_of_path(self, data, path_list):
        """
        data: json格式的数据, 或者dict
        path_list: 一个路径列表, 列表中的各个元素是json_data的节点信息
        """
        alias_of_data = data
        for path in path_list:
            alias_of_data = alias_of_data[path]
        debug_str = "以上面响应日志为数据对象,根据路径列表信息{},提取的数据信息为{}".format(path_list, str(alias_of_data))
        logger.debug(debug_str)
        return alias_of_data

    def update_data(self, json_data):
        self.data = json_data

    def get_value_of_complex_key(self, data, key):
        # 主动将数据更新到实例中，这是必须的行为
        self.update_data(data)
        if "_" not in key:
            res = self.find_all_values_path_by_key(key)  # 预期返回一个二维列表
            logger.debug("使用普通key(即不带下划线)方式查找出的值所对应的node节点路径信息列表为{}".format(res))
            if len(res) == 0:
                raise RuoyiError("can_not_find_key_in_json_data", key=key)
            elif len(res) > 1:
                raise self.KeyError("find_too_many_key", key_info=res)
            else:
                pass
            target_obj = self.get_value_of_path(data, res[0])
        else:
            key_list = key.split("_")

            res = self.find_all_values_path_by_key(key_list[-1])
            logger.debug("使用complex_key(即带下划线)方式查找出的值所对应的node节点路径信息列表为{}".format(res))

            # 选取出路径节点列表, 如果选不到那么就抛出一场
            # 大致场景为res = [["data", "id"], ["data", "sourceNode", "id"]], 然后传入key比如为"sourceNode_id"
            # 即key_list = ["sourceNode", "id""]
            target_path_str_list = " ".join(key_list)

            logger.debug("用户在业务脚本层传入的key的关键信息为" + target_path_str_list)

            target_obj_list = []
            for item in res:
                per_res = " ".join(item)
                if per_res.endswith(target_path_str_list):
                    target_obj_list.append(item)
            if len(target_obj_list) == 1:
                target_obj = self.get_value_of_path(data, target_obj_list[0])
            else:
                raise self.FindKeyError()

        # 提取路径节点列表, 预期res为[["a", "b", "c"]]
        return target_obj

    def edit(self, json_data: dict=None, **kwargs):
        if json_data is None:
            raise
        if "update" in kwargs.keys():
            update_content = kwargs["update"]
            json_data.update(update_content)

        if "add" in kwargs.keys():
            pass
        if "mod" in kwargs.keys():
            pass
        if "rmv" in kwargs.keys():
            # ["当前节点_jsonpath"]
            pass
