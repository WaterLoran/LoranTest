import json
import requests
from core.loran_hook.logger.logger_interface import logger
from config.environment import Environment
from core.exception import *
import pprint


class SingletonMeta(type):
    """
    功能: 实现一个单例模式的基类,只要子类集成这个类即可实现单例模式
    目的: 解决日志管理器在多处调用都能保证是同一个
    https://refactoringguru.cn/design-patterns/singleton/python/example#example-0
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Token(metaclass=SingletonMeta):
    def __init__(self):
        # 用于记录logger的配置信息
        self._token = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value


class BaseApi:
    def __init__(self):
        env = Environment()
        self.base_url = env.base_url
        self.username = env.username
        self.password = env.password
        self.token = None
        self.cookie = None

    def get_token(self):
        self._get_token()

    def _get_token(self):
        # 获取验证码的uuid
        url = "dev-api/captchaImage"
        rsp = requests.request("get", self.base_url + url)
        rsp_json = rsp.json()
        uuid = rsp_json["uuid"]

        url = "dev-api/login"
        login_json = {
            "username": self.username,
            "password": self.password,
            "code": "888",
            "uuid": uuid
        }
        rsp = requests.request("post", self.base_url + url, json=login_json)
        rsp_json = rsp.json()
        print("rsp_json", rsp_json)
        self.token = rsp_json["token"]
        self.cookie = self.token
        return self.cookie

    def _set_token(self, request_infos):
        global_token = Token()
        if global_token.token is None:
            global_token.token = self._get_token()

        self.token = global_token.token  # 从单利模式的全局变量处获得
        logger.debug("全局token是{}".format(self.token))
        Authorization = f"Bearer {self.token}"
        if request_infos.get("headers"):
            request_infos["headers"].update({"Authorization": Authorization})
            logger.debug("Heaeders是{}".format(request_infos["headers"]))
        else:
            import copy
            request_infos["headers"] = {}
            request_infos["headers"].update({"Authorization": Authorization})
            logger.debug("Heaeders是{}".format(request_infos["headers"]))
        return request_infos

    def send(self, method="", url="", **kwargs):
        kwargs = self._set_token(kwargs)
        self.log_req_info_before_request(url=url, method=method, **kwargs)
        rsp = requests.request(method, self.base_url + url, **kwargs)
        try:
            rsp_json = rsp.json()
            rsp_res = rsp_json
            logger.info(f"{url}接口的响应::rsp_data: " + json.dumps(rsp_json, indent=2, ensure_ascii=False))
        except:
            rsp_res = rsp.__dict__
            logger.info(f"{url}接口的响应(非常规响应而是可能会带有二进制文件的)::rsp_dict: " + str(rsp_res))
        return rsp_res

    def log_req_info_before_request(self, **kwargs):
        req_url = kwargs["url"]

        req_body_list = ["json", "form_data", "params", "data", "req_body"]
        for body in req_body_list:
            if body in kwargs.keys():
                body_value = kwargs[body]
                if isinstance(body_value, dict):
                    logger.info(f"{req_url}接口的请求体为::: " + json.dumps(body_value, indent=2, ensure_ascii=False))
                else:
                    logger.info(f"{req_url}接口的请求体为::: " + str(body_value))

                    # TODO 需要针对列表类型, 使用pprint来打印
        logger.debug("")


base = BaseApi()
base.get_token()

