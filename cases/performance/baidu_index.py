# -*- coding: utf-8 -*-
# @Pjname ;ApiDome
# @Time   :2023/09/19/22:19
# @Author :WaterLoran
# @File   :LocustDome.py
import time
import sys
from locust import HttpUser, task, TaskSet, events


class UserBehavior(HttpUser):

    def on_start(self):
        print("运行压测前置条件")

    def get_response(self, response):
        """
        获取返回
        :param response:请求返回对象
        :return:
        """
        start_time = int(time.time())
        if response.status_code == 200:
            events.request_success.fire(
                request_type="recv",
                name=sys._getframe().f_code.co_name,
                response_time=int(time.time() - start_time) * 1000,
                response_length=0
            )
        else:
            events.request_failure.fire(
                request_type="recv",
                name=sys._getframe().f_code.co_name,
                response_time=int(time.time() - start_time) * 1000,
                response_length=0,
                exception=f"Response Code Error! Code:{response.content}"
            )

    @task(1)
    def test_get(self):
        self.client.get("http://www.baidu.com", name="打开百度首页")

    @task(1)
    def test_post(self):
        """由于没有免费的post接口暂时使用百度搜索"""
        self.client.get("http://www.baidu.com?wd=testerhome", name="使用百度搜索")


class WebUser(TaskSet):
    """性能测试配置 换算配置"""
    host = "http://www.baidu.com"
    task_set = UserBehavior  # Testcase类
    min_wait = 100
    max_wait = 300


# 执行该脚本的脚本
# locust -f .\baidu_index.py  --host=--host=http://www.baidu.com --web-host="127.0.0.1"
