"""
角色管理-用户授权 API 封装
对应 RuoYi SysRoleController: allocatedList, unallocatedList, cancel, cancelAll, selectAll
"""
from core.logic import *
import allure


@Api.urlencoded
@allure.step("已分配用户列表-lst_role_allocated_users")
def lst_role_allocated_users(
    roleId="",
    pageNum=1,
    pageSize=10,
    userName="",
    phonenumber="",
    **kwargs,
):
    req_url = "/dev-api/system/role/authUser/allocatedList"
    req_method = "GET"
    req_params = {
        "roleId": "",
        "pageNum": 1,
        "pageSize": 10,
        "userName": "",
        "phonenumber": "",
    }
    rsp_check = {"msg": "查询成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("未分配用户列表-lst_role_unallocated_users")
def lst_role_unallocated_users(
    roleId="",
    pageNum=1,
    pageSize=10,
    userName="",
    phonenumber="",
    **kwargs,
):
    req_url = "/dev-api/system/role/authUser/unallocatedList"
    req_method = "GET"
    req_params = {
        "roleId": "",
        "pageNum": 1,
        "pageSize": 10,
        "userName": "",
        "phonenumber": "",
    }
    rsp_check = {"msg": "查询成功", "code": 200}
    return locals()


@Api.json
@allure.step("取消授权用户-cancel_auth_user")
def cancel_auth_user(userId=None, roleId=None, **kwargs):
    req_url = "/dev-api/system/role/authUser/cancel"
    req_method = "PUT"
    req_json = {"userId": None, "roleId": None}
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("批量取消授权用户-cancel_auth_user_all")
def cancel_auth_user_all(roleId="", userIds=None, **kwargs):
    if userIds is None:
        userIds = []
    req_url = "/dev-api/system/role/authUser/cancelAll"
    req_method = "PUT"
    req_params = {"roleId": "", "userIds": userIds}
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("批量授权用户-select_auth_user_all")
def select_auth_user_all(roleId="", userIds=None, **kwargs):
    if userIds is None:
        userIds = []
    req_url = "/dev-api/system/role/authUser/selectAll"
    req_method = "PUT"
    req_params = {"roleId": "", "userIds": userIds}
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()
