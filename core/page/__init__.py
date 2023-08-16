import json
import functools
import jsonpath
from .web_driver import WebDriver
from .base_web_page import WebBasePage
from core.loran_hook.logger.logger_interface import logger


class Page:

    def get_page_data(self, func, **kwargs):
        page_data = func(**kwargs)
        logger.info("PAGE页面 ==> " + func.__name__)
        logger.debug(json.dumps(page_data, indent=2, ensure_ascii=False))
        return page_data

    def organization_location(self, page_data_location_str, append_location_dict):
        last_location = ""
        if "add" in append_location_dict.keys():
            add_location = append_location_dict["add"]
            last_location = page_data_location_str + add_location
        return last_location

    def judge_action_data_type(self, page_node_input):
        action_data_type = "basic"
        logger.debug("judge_action_data_type函数输入的page_node_input变量为" + str(page_node_input))
        element_key = page_node_input[0]  # 入参的名称
        element_value = page_node_input[1]  # 入参的值
        if isinstance(element_value, str):
            action_data_type = "string"
        elif isinstance(element_value, dict):
            action_data_type = "dict"
        else:
            raise
        logger.debug("入参的类型是" + action_data_type)
        return action_data_type

    def extract_action_info(self, page_node_input, page_data):

        action_info = {}

        action_data_type = Page().judge_action_data_type(page_node_input)
        if action_data_type == "string":
            # 判断page_node_input的值是click(关键字) 还是其他字符串
            input_key = page_node_input[0]
            input_value = page_node_input[1]
            logger.debug(f"输入的信息,key为{input_key}, value为{input_value}")

            jsonpath_regex = f"$..{input_key}"
            tartget_obj = jsonpath.jsonpath(page_data, jsonpath_regex)[0]
            location = tartget_obj["location"]  #TODO 需要针对这里的场景做一个前作的cation_info的提取, 并且追加到action_info中
            loca_way = location[0]
            loca_expression = location[1]

            logger.debug("提取到的page_data的node信息为" + json.dumps(tartget_obj, indent=2, ensure_ascii=False))

            if input_value.upper == "" or input_value.upper == None:
                pass  # TODO 设计元素的默认操作
            elif input_value.upper() == "CLICK":
                action = "click"
                action_info.update({
                    "loca_way": loca_way,
                    "loca_expression": loca_expression,
                    "action": action
                })
            elif input_value.upper() == "DRAG_TO_BUTTOM":
                action = "drag_to_buttom"
                action_info.update({
                    "loca_way": loca_way,
                    "loca_expression": loca_expression,
                    "action": action
                })
            else:  # 表示除了CLICK的之外的其他字符串
                # 这种场景需要结合元素的类型, 比如input, 或者其他的来决定
                tartget_obj_type = tartget_obj["type"]
                if tartget_obj_type == "input":  # 表示钙元素是一个可输入的框, 并且业务脚本层输入一个字符串, 即表示要讲这个字符串输入到输入框中
                    default_action = tartget_obj["default_action"]  # 有可能为type , 也有可能为input
                    action = default_action  # 通常情况下是 "type", 有些场景需要输入后再去回车就是["type", "enter"]
                    input_content = input_value  # 表示业务脚本层输入的就是内容
                    action_info.update({
                        "loca_way": loca_way,
                        "loca_expression": loca_expression,
                        "action": action,
                        "input_content": input_content
                    })

        elif action_data_type == "dict":
            input_key = page_node_input[0]
            jsonpath_regex = f"$..{input_key}"
            tartget_obj = jsonpath.jsonpath(page_data, jsonpath_regex)[0]
            location = tartget_obj["location"]
            loca_way = location[0]
            loca_expression = location[1]

            input_dict = page_node_input[1]

            if "action" not in input_dict.keys():
                raise
            action = input_dict["action"]
            if "append_location" in input_dict.keys():
                append_location_dict = input_dict["append_location"]
                loca_expression = Page().organization_location(loca_expression, append_location_dict)

            action_info.update({
                "loca_way": loca_way,
                "loca_expression": loca_expression,
                "action": action
            })

        logger.debug(f"根据{str(page_node_input)}提取到的操作信息为" + json.dumps(action_info, indent=2, ensure_ascii=False))
        return action_info

    def action(self, **kwargs):
        cur_page = WebBasePage()
        loca_way = kwargs["loca_way"]
        loca_expression = kwargs["loca_expression"]
        action = kwargs["action"]
        if isinstance(action, str):
            if action.upper() == "CLICK":
                logger.info(f"将以{loca_way}方式以 {loca_expression} 值去查找元素, 然后点击")
                cur_page.find_and_click(loca_way, loca_expression)

            elif action.upper() == "INPUT" or action.upper() == "TYPE":
                if "input_content" not in kwargs.keys():
                    raise  # TODO 这里要封装没有对应key的异常
                input_content = kwargs["input_content"]
                logger.info(f"将以{loca_way}方式以 {loca_expression} 值去元素去定位, 然后输入字符串 {input_content} ")
                cur_page.find_and_send(loca_way, loca_expression, input_content)

            elif action.upper() == "DRAG_TO_BUTTOM":
                logger.info(f"将以{loca_way}方式以 {loca_expression} 值去查找元素, 然后拖拽到底部")
                cur_page.find_and_drag_to_buttom(loca_way, loca_expression)

            elif action.upper() == "MOVE_HERE":
                logger.info(f"将以{loca_way}方式以 {loca_expression} 值去元素查找, 然后移动鼠标到这个位置")
                cur_page.find_and_move_here(loca_way, loca_expression)
            else:
                pass

        if isinstance(action, list):
            if action == ["type", "enter"]:
                if "input_content" not in kwargs.keys():
                    raise  # TODO 这里要封装没有对应key的异常
                input_content = kwargs["input_content"]
                logger.info(f"将以{loca_way}方式以 {loca_expression} 值去元素去定位, 然后输入字符串 {input_content} ")
                cur_page.find_and_send_then_enter(loca_way, loca_expression, input_content)

    def do_all_web_operation(self, page_data, operation_list):
        for page_node_input in operation_list:
            action_info = Page().extract_action_info(page_node_input, page_data)  # 获得一个步骤的操作信息, 包括(定位信息, 操作行为, 元素描述)
            Page().action(**action_info)  # 做实际一个步骤的操作, 定位元素,显隐性等待,浏览器行为(输入或者点击, 或者拖动), 日志(根据page的描述信息, 定位信息, 和操作)

    @classmethod
    def base(self, func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            """我是 wrapper 的注释"""

            # 做入参信息的提取, 后续需要针对关键字信息践行提取
            operation_list = []
            for key, value in kwargs.items():
                operation_list.append([key, value])

            ## 从记录page数据的函数中获取所有的数据, 并解析出来
            page_data = Page().get_page_data(func)

            ## 对入参进行遍历, 依次从page数据中取出对应元素, 识别, 并做对应的操作
            Page().do_all_web_operation(page_data, operation_list)

        return wrapper
