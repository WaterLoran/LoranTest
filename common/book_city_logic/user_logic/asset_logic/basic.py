from core.logic import *
import allure


@Api.urlencoded
@allure.step("查看用户资产-lst_user_asset")
def lst_user_asset(**kwargs):
    req_method = "GET"
    req_url = "/user/asset"
    req_params = {}
    return locals()
