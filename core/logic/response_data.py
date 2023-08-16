import pytest_check
import jsonpath
import json
import copy
from core.loran_hook.logger.logger_interface import logger
from core.exception import RuoyiError
from .json_data import JsonData


class ResponeseData(JsonData):

    def check_all_expect(self, data, check_info):

        def echo_debug_locate_info(rsp_data):
            try:
                rsp_code = rsp_data["code"]
                logger.error("响应码为"+rsp_code)
            except:
                pass
            try:
                rsp_message = rsp_data["message"]
                logger.error("响应对应的堆栈错误信息为为"+rsp_message)
            except:
                pass

        def judge_comparator_type(comparator):
            compare_dict = {
                "equal": ["==", "eq", "equal"],
                "not_equal": ["!=", "not_equal", "not_eq"],
                "greater": [">", "lg", "larger", "greater"],
                "less": ["<", "smaller", "less"],
                "greater_equal": [">=", "greater_equal"],
                "less_equal": ["<=", "less_equal"],
                "in": ["in"],
                "not_in": ["not_in"],
                "include": ["include"],
                "not_include": ["not_include"],
            }
            for key, value in compare_dict.items():
                if comparator in value:
                    return key
            raise

        def assert_action(compared_obj, compare_type, target):
            logger.debug("\n    真实指定的响应对象为 {}, 类型为{}\n    比较方式为 {},\n    期望对象为 {}, 类型为{}".format
                         (compared_obj, type(compared_obj), compare_type, target, type(target)))
            if compare_type == "equal":
                pytest_check_result = pytest_check.equal(compared_obj, target)
            elif compare_type == "not_equal":
                pytest_check_result = pytest_check.not_equal(compared_obj, target)
            elif compare_type == "greater":
                pytest_check_result = pytest_check.greater(compared_obj, target)
            elif compare_type == "greater_equal":
                pytest_check_result = pytest_check.greater_equal(compared_obj, target)
            elif compare_type == "less":
                pytest_check_result = pytest_check.less(compared_obj, target)
            elif compare_type == "less_equal":
                pytest_check_result = pytest_check.less_equal(compared_obj, target)
            elif compare_type == "in":
                pytest_check_result = pytest_check.is_in(compared_obj, target)
            elif compare_type == "not_in":
                pytest_check_result = pytest_check.is_not_in(compared_obj, target)
            elif compare_type == "include":
                pytest_check_result = pytest_check.is_in(target, compared_obj)
            elif compare_type == "not_include":
                pytest_check_result = pytest_check.is_not_in(target, compared_obj)
            else:
                raise
            if pytest_check_result:
                logger.debug("pytest_check断言结果为真")
                return True
            else:
                logger.error("pytest_check断言结果为假  ==>  0  <== False ==> 假 <==")
                return False

        def check_one_expect_by_key(data, single_check):
            name, comparator, target = single_check  # target 为期望值
            compared_obj = self.get_value_of_complex_key(data, name)
            compare_type = judge_comparator_type(comparator)
            if not assert_action(compared_obj, compare_type, target):
                echo_debug_locate_info(data)

        def check_one_expect_by_regex(data, single_check):
            jsonpath_regex, comparator, target = single_check
            try:
                compared_obj = jsonpath.jsonpath(data, jsonpath_regex)[0]
            except Exception as err:
                logger.error(json.dumps(data, indent=2, ensure_ascii=False))
                logger.error("jsonpath_regex为  " + str(jsonpath_regex))
                logger.error("最经常出现的问题是jsonpath表达式不正确, 比如 .. 点号数量少了一个")
                raise RuoyiError("real_rsp_jsonpath_error")
            try:
                compare_type = judge_comparator_type(comparator)
            except Exception as err:
                raise RuoyiError("no_such_comparator_type")
            if not assert_action(compared_obj, compare_type, target):
                echo_debug_locate_info(data)

        def judge_expression_type(expression):
            json_path_expression = expression

            expression_type = "key"
            import string
            for i in json_path_expression:
                if i not in string.ascii_lowercase + string.ascii_uppercase + "_":
                    expression_type = "regex"
            return expression_type

        logger.info("开始用户定义的脚本层数据的断言操作")
        logger.debug("业务层脚本用户自定义的主动断言check_info为" + str(check_info))
        # 判断传入的参数是否为一维列表,如果是则主动加一层, 将其变成2维列表
        change_two_dimensional_flag = False
        for element in check_info:
            if not isinstance(element, list):
                change_two_dimensional_flag = True
                break
        if change_two_dimensional_flag:
            check_info = [check_info]

        # 循环对check列表项中的check项去做检查
        for single_check in check_info:
            logger.debug("业务脚本层单个断言信息::single_check" + str(single_check))
            expression_type = judge_expression_type(single_check[0])  # single_check[0]表示期望检查的complex_key或者regex
            if expression_type == "key":
                check_one_expect_by_key(data, single_check)
            elif expression_type == "regex":
                check_one_expect_by_regex(data, single_check)
            else:
                raise
        logger.info("结束用户定义的脚本层数据的断言操作")


    def fetch_all_value(self, data, fetch_info):

        def fetch_one_value_by_regex(data, var_info):
            reg_dict = var_info[0]
            key = var_info[1]
            json_path_reg = var_info[2]
            logger.debug("被查找对象为::" + str(data))
            reg_dict[key] = jsonpath.jsonpath(data, json_path_reg)[0]
            logger.debug(f"使用regex表达式{json_path_reg}方式查找出的值为{reg_dict[key]}")

            return reg_dict[key]

        def fetch_one_value_by_key(data, var_info):
            reg_dict = var_info[0]
            key = var_info[1]
            json_path_key = var_info[2]
            reg_dict[key] = self.get_value_of_complex_key(data, json_path_key)
            return reg_dict[key]

        def judge_expression_type_fetch(var_info):
            json_path_expression = var_info[2]

            expression_type = "key"
            import string
            for i in json_path_expression:
                # 这里的校验包含下划线是为了支持complex_key
                if i not in string.ascii_lowercase + string.ascii_uppercase + "_":
                    expression_type = "regex"
            logger.debug("提取入参的表达式为:{}, 类型为{}".format(json_path_expression, expression_type))
            return expression_type

        logger.debug("开始提取响应信息")
        # 如果传入的参数为单层列表, 则将其转变为二维列表
        change_two_dimensional_flag = False
        for element in fetch_info:
            if not isinstance(element, list):
                change_two_dimensional_flag = True
                break
        if change_two_dimensional_flag:
            logger.debug("检测到入参为单层列表，将对该入参转为二维列表，即统一格式为双层列表入参")
            fetch_info = [fetch_info]

        fetch_var_list = []
        for info in fetch_info:
            # 判断传入的判断式是正则表达式, 还是普通的key(只由26个大小写字母组合而成)
            expression_type = judge_expression_type_fetch(info)
            if expression_type == "regex":
                fetch_var_list.append(fetch_one_value_by_regex(data, info))
            elif expression_type == "key":
                fetch_var_list.append(fetch_one_value_by_key(data, info))
            else:
                raise
        logger.info("提取的目标信息为:{}".format(fetch_var_list))
        logger.debug("结束提取响应信息")
        return fetch_var_list

    def check_rsp_check(self, req_body, rsp_data, rsp_check):
        def judge_api_check_expression_type(expression):
            expression_type = "string"
            if "$" in expression:
                expression_type = "regex"
            return expression_type

        pytest_check_cache = []
        def traverse_json(check_data, real_rsp, path):
            nonlocal pytest_check_cache
            if isinstance(check_data, tuple):
                logger.error("当前的被识别为tuple的数据为" + str(check_data))
                logger.error("请检查rsp_check的后面是否还有一个小括号, 这将会被框架将 rsp_check 数据识别为元组")
            for key, value in check_data.items():
                if isinstance(value, dict):
                    t_path = copy.deepcopy(path)
                    t_path.append(key)
                    if key not in real_rsp.keys():
                        raise RuoyiError("real_rsp_has_no_such_field", key=key, value=value)
                    traverse_json(value, real_rsp[key], t_path)  # 同步递归real_rsp的响应信息
                elif isinstance(value, list):  # 有可能这个就是根节点, 这个就是要比较的数据
                    for i in range(len(value)):
                        item = value[i]
                        if isinstance(item, dict):
                            t_path = copy.deepcopy(path)
                            t_path.append(key)
                            traverse_json(item, real_rsp[i], t_path)
                        else:
                            logger.error("列表中只允许有字典, 不允许其他类型, 如果出现这个报错, 请联系冯进聪修定位修改代码")
                            # TODO 待决定这里是否要增加 ["location_info", "more_action"]的场景, 用于表示获取到数据之后, 多做一点动作
                            raise
                else:  # 表示检查的对象是字符串了，也就是有两种可能，一种为普通的字符串，一种为jsonpath的表达式
                    t_path = copy.deepcopy(path)
                    t_path.append(key)
                    # 判断是普通字符串, 还是regex
                    expression_type = judge_api_check_expression_type(value)
                    if expression_type == "string":
                        logger.debug("根据api层预定义的单个check信息做断言")
                        logger.debug("取值的表达式类型为string")
                        check_type = "string"
                        except_obj = value
                        if key not in real_rsp.keys():
                            raise RuoyiError("real_rsp_has_no_such_field", check_key=key)
                        target_obj = real_rsp[key]
                        check_obj = {
                            "check_type": check_type,
                            "except_obj": except_obj,
                            "target_obj": target_obj,
                            "path": t_path
                        }
                        pytest_check_cache.append(check_obj)
                    elif expression_type == "regex":
                        logger.debug("根据api层预定义的单个check信息做断言")
                        logger.debug("取值的表达式类型为regex")
                        logger.debug("req_body: " + json.dumps(req_body))
                        logger.debug("value: " + str(value))

                        try:  #请求体中不含有目标jsonpath路径的异常情况
                            except_obj = jsonpath.jsonpath(req_body, value)[0]
                        except Exception as err:
                            raise RuoyiError("req_body_jsonpath_error", json_path=value)
                        try:
                            target_obj = real_rsp[key]
                        except Exception as err:
                            raise RuoyiError("real_rsp_jsonpath_error", real_rsp_key=key)
                        check_obj = {
                            "check_type": "regex",
                            "except_obj": except_obj,
                            "target_obj": target_obj,
                            "path": t_path
                        }
                        pytest_check_cache.append(check_obj)

        logger.info("========  开始根据API数据层定义的rsp_check做自动断言  ========")

        # 仅仅对响应为成功的场景做自动断言操作
        if rsp_data["code"] != "SUCCESS":
            # 获取message信息
            # 获取code信息
            try:
                rsp_code = rsp_data["code"]
                logger.error("响应码为"+rsp_code)
            except:
                pass
            try:
                rsp_message = rsp_data["message"]
                logger.error("响应对应的堆栈错误信息为为"+rsp_message)
            except:
                pass
            assert False


        try:
            logger.debug("API层预定义的rsp_check的信息为" + json.dumps(rsp_check, indent=2, ensure_ascii=False))
            traverse_json(rsp_check, rsp_data, [])
        except Exception as err:
            logger.error("根据API数据层定义的rsp_check同步去做数据比较时候出现异常,请排查响应体中 是否有 和API层定义的期望json 同样的路径结构" + str(err))
            logger.debug(err)
            pytest_check.is_true(False)  # 主动捕捉异常并抛出pytest_check的异常, 并且不能影响参数的返回

        for check_obj in pytest_check_cache:
            check_type = check_obj["check_type"]
            except_obj = check_obj["except_obj"]
            target_obj = check_obj["target_obj"]
            path = check_obj["path"]

            logger.debug("需要断言的总数量为" + str(len(pytest_check_cache)))
            logger.debug("====  开始对单个API层预定义的检查项做断言  ====")

            logger.debug("断言的类型为{}".format(check_type))
            logger.debug("预定义期望的路径为{}".format(path))

            except_debug_str = "API数据层预定义的期望except_obj为{}, 数据类型为{}".format((except_obj), str(type(except_obj)))
            logger.debug(except_debug_str)
            target_debug_str = "实际的响应信息的target_obj为{}, 数据类型为{}".format((target_obj), str(type(target_obj)))
            logger.debug(target_debug_str)
            pytest_check_result = pytest_check.equal(except_obj, target_obj)
            if not pytest_check_result:
                logger.error("APi数据层预定义的断言结果为假  ==>  0  <== False ==> 假 <==")
            logger.debug("====  结束对单个API层预定义的检查项做断言  ====\n")

        logger.info("========  结束根据API数据层定义的rsp_check做自动断言  ========\n")
        pass
