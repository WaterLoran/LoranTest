"""
发送飞书通知
"""
import json
import logging
import time
import datetime
import requests
import urllib3
from plugin.models import TestMetrics
from config import notify

urllib3.disable_warnings()

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


def is_not_null_and_blank_str(content):
    """
  非空字符串
  :param content: 字符串
  :return: 非空 - True，空 - False
  """
    return bool(content and content.strip())


class FeiShuTalkChatBot:
    """飞书机器人通知"""

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics

    def send_text(self, msg: str):
        """
    消息类型为text类型
    :param msg: 消息内容
    :return: 返回消息发送结果
    """
        data = {"msg_type": "text", "at": {}}
        if is_not_null_and_blank_str(msg):  # 传入msg非空
            data["content"] = {"text": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        logging.debug('text类型：%s', data)
        return self.post()

    def post(self):
        """
        发送消息（内容为UTF-8编码格式）
        :return: 返回消息发送结果
        """
        rich_text = {
            "email": "1696746432@qq.com",
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"{notify.project_name}",
                        "content": [
                            [
                                {
                                    "tag": "a",
                                    "text": "测试报告",
                                    "href": "http://43.142.85.209:8083/index.html"
                                },
                                {
                                    "tag": "at",
                                    # "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb"
                                    "user_id": "all"
                                    # "text":"冯进聪"
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": f"测试执行者： "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{notify.tester_name}"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": f"测试环境："
                                },
                                {
                                    "tag": "text",
                                    "text": f"{notify.env}"
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": "成   功   率 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.pass_rate} %"
                                }],  # 成功率

                            [{
                                "tag": "text",
                                "text": "成功用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.passed}"
                                }],  # 成功用例数

                            [{
                                "tag": "text",
                                "text": "失败用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                                }],  # 失败用例数
                            [{
                                "tag": "text",
                                "text": "异常用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                                }],  # 损坏用例数
                            [{
                                "tag": "text",
                                "text": "阻塞用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.broken}"
                                }],  # 阻塞用例数
                            [{
                                "tag": "text",
                                "text": "跳过用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.skipped}"
                                }],  # 跳过用例数
                            [
                                {
                                    "tag": "text",
                                    "text": "时  间 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
                                }
                            ],

                            # [
                            #     {
                            #         "tag": "img",
                            #         "image_key": "d640eeea-4d2f-4cb3-88d8-c964fab53987",
                            #         "width": 300,
                            #         "height": 300
                            #     }
                            # ]
                        ]
                    }
                }
            }
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        post_data = json.dumps(rich_text)
        print("post_data", post_data)
        response = requests.post(
            notify.lark_webhook,
            headers=headers,
            data=post_data,
            verify=False
        )
        print("response", response)
        result = response.json()
        print("response.json()", response.json())

        if result.get('StatusCode') != 0:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            result_msg = result['errmsg'] if result.get('errmsg', False) else '未知异常'
            error_data = {
                "msgtype": "text",
                "text": {
                    "content": f"[注意-自动通知]飞书机器人消息发送失败，时间：{time_now}，"
                               f"原因：{result_msg}，请及时跟进，谢谢!"
                },
                "at": {
                    "isAtAll": False
                }
            }
            logging.error("消息发送失败，自动通知：%s", error_data)
            requests.post(notify.lark_webhook, headers=headers, data=json.dumps(error_data))
        return result
