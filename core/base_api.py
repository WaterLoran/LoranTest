import json
import requests
from core.logger.logger_interface import logger
from config.environment import Environment


class BaseApi:
    def __init__(self, role=None):
        env = Environment()
        self.base_url = env.base_url
        self.token = None
        self.role = role

    def _get_token(self, role=None):
        if role != "admin" and role != "client":
            raise ValueError
        url = {
            "admin": "admin/auth/login",
            "client": "wx/auth/login",
        }
        data = {
            "admin": {"username": "admin123", "password": "admin123"},
            "client": {"username": "user123", "password": "user123"},
        }
        req_token = {
            "admin": "X-Litemall-Admin-Token",
            "client": "X-Litemall-Token",
        }
        req = requests.request("post", self.base_url + url[role], json=data[role])
        self.token = {req_token[role]: req.json()["data"]["token"]}
        pass

    def _set_token(self, request_infos):
        if self.token is None:
            self._get_token(role=self.role)

        if request_infos.get("headers"):
            request_infos["headers"].update(self.token)
        else:
            request_infos["headers"] = self.token
        return request_infos

    def send(self, method="", url="", **kwargs):
        kwargs = self._set_token(kwargs)
        rsp = requests.request(method, self.base_url + url, **kwargs)
        rsp_json = rsp.json()
        logger.debug(f"BaseApi::send ==> {url}接口的响应为{json.dumps(rsp_json, indent=2, ensure_ascii=False)}")
        return rsp_json

