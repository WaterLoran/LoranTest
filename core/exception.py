from core.loran_hook.logger.logger_interface import logger

class RuoyiError(Exception):
    def __init__(self, error_key, **kwargs):
        error_dict = {
            "real_rsp_has_no_such_field": "代码逻辑中尝试使用指定的key去获取对应的值，但是没有找到对应的key，所以请排查真实的响应信息和传入的key. ",
            "req_body_jsonpath_error": "填充后的请求体重a中不含有该jsonpath路径的相关信息. ",
            "real_rsp_jsonpath_error": "真实响应中没有指定的key路径. 可能为以下原因: 1,虽然jsonpath正确, 但响应是异常响应. 2,响应为成功响应, 但编写的jsonpath错误. ",
            "can_not_find_key_in_json_data": "在json体中找不到名字为key的路径. ",
            "get_token_failed": r"可能存在以下下原因导致获取token失败：1.登录的URL更换 2. 账号密码传输前不加密 3.token的在响应中的位置发生变更 4.响应中不携带token 5.其他可能原因请找开发排查. ",
            "no_such_comparator_type": r"不存在此种比较符, 排查思路: 1, 当前框架不支持该比较符号即为开发. 2, 用户使用了不合理并且以后也不会支持的比较符. 3,在框架代码中搜索judge_comparator_type. ",
            "api_data_has_no_such_field": "API数据层所编写的数据中没有这个字段,排查思路: 1,排查API数据层. 2,在框架代码中搜索get_api_data. ",
            "req_body_find_too_many_key": "在req_body中发现了两个或以上的同名的key(不含下划线), 排查思路: 1, 查看req_body中是否有同名的key. 2, 请求体发生变更. 3,指定key编写错误. ",
            "rsp_data_find_too_many_key": "在rsp_data_中发现了两个或以上的同名的key, 排查思路: 1, 查看rsp_data_中是否有同名的key. 2,指定key编写错误. ",
            "the_api_data_is_none": "返回的Api数据是None, 排查思路: 1, 请检查APi数据层是否编写return locals(). 2, 有可能你定义的是sphere类的logic, 即由多个logic组成的, 该情况不用return,但是gailogic不能用api来装饰",
            "can_not_find_key_in_req_data": "在请求体中找不到对应的key, 排查思路: 1, 排查范围包括所有可能需要填充的请求体比如req_body, req_params. 2, 有可能该请求不需要做入参填充, APi数据层需要编写fill_req_body=False. 3, 该key确实在请求体中找不到. 4, 该key编写错误"
        }
        self.error_info = error_dict[error_key]
        for key, value in kwargs.items():
            key_info = "key: {}, value: {}\n".format(key, value)
            self.error_info += key_info

        logger.error(str(self.error_info))

    def __str__(self):
        return repr(self.error_info)
