#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/28 15:30
# @Author : 余少琪
"""
钉钉通知封装
"""
import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, Text
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink
from plugin.local_info import get_host_ip
from plugin.allure_data.allure_report_data import AllureFileClean, TestMetrics
from config.notify import *


class DingTalkSendMsg:
    """ 发送钉钉通知 """
    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics
        self.timeStamp = str(round(time.time() * 1000))

    def xiao_ding(self):
        sign = self.get_sign()
        print("=============================>>>>>   sign", sign)
        # 从yaml文件中获取钉钉配置信息
        webhook = ding_talk_webhook + "&timestamp=" + self.timeStamp + "&sign=" + sign
        return DingtalkChatbot(webhook)

    def get_sign(self) -> Text:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        string_to_sign = f'{self.timeStamp}\n{ding_talk_secret}'.encode('utf-8')
        hmac_code = hmac.new(
            ding_talk_secret.encode('utf-8'),
            string_to_sign,
            digestmod=hashlib.sha256).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_text(
            self,
            msg: Text,
            mobiles=None
    ) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 艾特用户电话
        :return:
        """
        if not mobiles:
            self.xiao_ding().send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding().send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(
            self,
            title: Text,
            text: Text,
            message_url: Text,
            pic_url: Text
    ) -> None:
        """
        发送link通知
        :return:
        """
        self.xiao_ding().send_link(
                title=title,
                text=text,
                message_url=message_url,
                pic_url=pic_url
            )

    def send_markdown(
            self,
            title: Text,
            msg: Text,
            mobiles=None,
            is_at_all=False
    ) -> None:
        """

        :param is_at_all:
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """

        if mobiles is None:
            self.xiao_ding().send_markdown(title=title, text=msg, is_at_all=is_at_all)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding().send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    @staticmethod
    def feed_link(
            title: Text,
            message_url: Text,
            pic_url: Text
    ) -> Any:
        """ FeedLink 二次封装 """
        return FeedLink(
            title=title,
            message_url=message_url,
            pic_url=pic_url
        )

    def send_feed_link(self, *arg) -> None:
        """发送 feed_lik """

        self.xiao_ding().send_feed_card(list(arg))

    def send_ding_notification(self):
        """ 发送钉钉报告通知 """
        # 判断如果有失败的用例，@所有人
        is_at_all = False
        if self.metrics.failed + self.metrics.broken > 0:
            is_at_all = True
        text = f"#### {project_name}自动化通知  " \
               f"\n\n>Python脚本任务: {project_name}" \
               f"\n\n>环境: TEST\n\n>" \
               f"执行人: {tester_name}" \
               f"\n\n>执行结果: {self.metrics.pass_rate}% " \
               f"\n\n>总用例数: {self.metrics.total} " \
               f"\n\n>成功用例数: {self.metrics.passed}" \
               f" \n\n>失败用例数: {self.metrics.failed} " \
               f" \n\n>异常用例数: {self.metrics.broken} " \
               f"\n\n>跳过用例数: {self.metrics.skipped}" \
               f" ![screenshot](" \
               f"https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png" \
               f")\n" \
               f" > ###### 127.0.0.1测试报告 [详情](http://127.0.0.1:9999/index.html) \n" \
               f" > ###### 测试报告 [详情](http://{get_host_ip()}:9999/index.html) \n"
        # TODO window下不能直接绑定固定IP
        DingTalkSendMsg(AllureFileClean().get_case_count()).send_markdown(
            title="【接口自动化通知】",
            msg=text,
            is_at_all=is_at_all
        )


if __name__ == '__main__':
    DingTalkSendMsg(AllureFileClean().get_case_count()).send_ding_notification()
    #  发送到钉钉的信息中,包含实际报告地址,在这之前需要先使用allure启动报告服务器, 命令是
    # window端命令 start allure open -h 192.168.0.101 -p 9999 E:\Develop\LoranTest\output\report
    # window端命令 start allure open -h 127.0.0.1 -p 9999 E:\Develop\LoranTest\output\report
