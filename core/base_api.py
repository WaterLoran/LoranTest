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


class Cookie(metaclass=SingletonMeta):
    def __init__(self):
        # 用于记录logger的配置信息
        self._cookie = None

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        self._cookie = value


class BaseApi:
    def __init__(self, role=None):
        env = Environment()
        self.base_url = env.base_url
        self.username = env.username
        self.password = env.password
        self.token = None
        self.cookie = None
        self.role = role

    def _get_token(self, role=None):
        if role != "admin" and role != "client":
            raise ValueError
        url = {
            # "admin": "viewer-service/auth/login",
            "admin": "api/authentication/login",
        }
        data = {
            "admin": {"username": self.username,
                      "password": self.password},
        }
        req_token = {
            "admin": "Auth-Token",
        }

        response = requests.request("post", self.base_url + url[role], json=data[role])
        # 此处为request所发请求，response中还另外携带connecttion，cookies，headers，request等信息
        rsp = response.content
        try:
            self.token = {req_token[role]: json.loads(rsp)["data"]["token"]}
            self.cookie = {"Cookie": "Auth-Token=" + json.loads(rsp)["data"]["token"]}
            self.token_content = json.loads(rsp)["data"]["token"]
        except Exception as err:
            raise RuoyiError("get_token_failed")
        return self.cookie

    def _set_token(self, request_infos):
        global_cookie = Cookie()
        if global_cookie.cookie is None:
            global_cookie.cookie = self._get_token(role=self.role)

        self.cookie = global_cookie.cookie  # 从单利模式的全局变量处获得
        Authorization = self.cookie["Cookie"].split("=")[1]  # 从cookie解析出token的内容, 用作Authorization
        logger.debug("全局Cookie是{}".format(self.cookie))
        if request_infos.get("headers"):
            request_infos["headers"].update(self.cookie)
            request_infos["headers"].update({"Authorization": Authorization})
            logger.debug("Heaeders是{}".format(request_infos["headers"]))
        else:
            import copy
            request_infos["headers"] = copy.deepcopy(self.cookie)
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
