import allure
from core.logic import Api


@Api.json
@allure.step("实例logic_1")
def add_xx_example(id="", **kwargs):
    req_method = "POST"
    url = "admin/goods/delete"
    body_data = {"id": None}
    return req_method, url, body_data


@Api.json
@allure.step("实例logic_1")
def rmv_xx_example(name="", **kwargs):
    req_method = "GET"
    url = "admin/goods/list"
    body_data = {
        "name": "",
        "order": "desc",
        "sort": "add_time"
    }
    return req_method, url, body_data

