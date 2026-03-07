"""
角色管理基础 API 封装
对应 RuoYi SysRoleController: list, getInfo, add, edit, changeStatus, remove, optionselect, export
"""
from core.logic import *
import allure


@Api.json
@allure.step("添加角色-add_role")
def add_role(
    roleName="",
    roleKey="",
    roleSort=None,
    status="0",
    menuIds=None,
    deptIds=None,
    menuCheckStrictly=True,
    deptCheckStrictly=True,
    remark="",
    **kwargs,
):
    if menuIds is None:
        menuIds = [1, 100, 1000]
    if deptIds is None:
        deptIds = []
    req_url = "/dev-api/system/role"
    req_method = "POST"
    req_json = {
        "roleName": "",
        "roleKey": "",
        "roleSort": None,
        "status": "0",
        "menuIds": menuIds,
        "deptIds": deptIds,
        "menuCheckStrictly": menuCheckStrictly,
        "deptCheckStrictly": deptCheckStrictly,
        "remark": "",
    }
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.json
@allure.step("修改角色-mod_role")
def mod_role(
    roleId=None,
    roleName="",
    roleKey="",
    roleSort=None,
    status="0",
    menuIds=None,
    deptIds=None,
    menuCheckStrictly=True,
    deptCheckStrictly=True,
    remark="",
    **kwargs,
):
    if menuIds is None:
        menuIds = []
    if deptIds is None:
        deptIds = []
    req_url = "/dev-api/system/role"
    req_method = "PUT"
    req_json = {
        "roleId": None,
        "roleName": "",
        "roleKey": "",
        "roleSort": None,
        "status": "0",
        "menuIds": menuIds,
        "deptIds": deptIds,
        "menuCheckStrictly": menuCheckStrictly,
        "deptCheckStrictly": deptCheckStrictly,
        "remark": "",
    }
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("查看角色列表-lst_role")
def lst_role(
    pageNum=1,
    pageSize=10,
    roleId=None,
    roleName="",
    roleKey="",
    status="",
    beginTime="",
    endTime="",
    **kwargs,
):
    req_url = "/dev-api/system/role/list"
    req_method = "GET"
    req_params = {
        "pageNum": 1,
        "pageSize": 10,
        "roleId": "",
        "roleName": "",
        "roleKey": "",
        "status": "",
        "params[beginTime]": beginTime,
        "params[endTime]": endTime,
    }
    rsp_check = {"msg": "查询成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("查看角色详情-lst_role_detail")
def lst_role_detail(roleId="", **kwargs):
    req_url = f"/dev-api/system/role/{roleId}"
    req_method = "GET"
    req_params = {}
    auto_fill = False
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.json
@allure.step("删除角色-rmv_role")
def rmv_role(role_id="", **kwargs):
    """删除单个或多个角色。批量删除时传入逗号分隔的 id，如 role_id='1,2,3'。"""
    req_url = f"/dev-api/system/role/{role_id}"
    req_method = "DELETE"
    req_json = {}
    rsp_check = {"msg": "操作成功", "code": 200}
    auto_fill = False
    return locals()


@Api.json
@allure.step("修改角色状态-change_role_status")
def change_role_status(roleId=None, status="0", **kwargs):
    req_url = "/dev-api/system/role/changeStatus"
    req_method = "PUT"
    req_json = {"roleId": None, "status": "0"}
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("角色下拉选项-lst_role_option_select")
def lst_role_option_select(**kwargs):
    req_url = "/dev-api/system/role/optionselect"
    req_method = "GET"
    req_params = {}
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("导出角色-export_role")
def export_role(roleName="", roleKey="", status="", **kwargs):
    req_url = "/dev-api/system/role/export"
    req_method = "POST"
    req_params = {"roleName": "", "roleKey": "", "status": ""}
    rsp_check = {"msg": "操作成功", "code": 200}
    # 导出接口可能返回文件流，测试时可 check=False
    return locals()
