"""
角色管理-数据权限 API 封装
对应 RuoYi SysRoleController: dataScope, deptTree
"""
from core.logic import *
import allure


@Api.json
@allure.step("修改角色数据权限-set_role_data_scope")
def set_role_data_scope(
    roleId=None,
    dataScope="1",
    deptIds=None,
    deptCheckStrictly=True,
    **kwargs,
):
    if deptIds is None:
        deptIds = []
    req_url = "/dev-api/system/role/dataScope"
    req_method = "PUT"
    req_json = {
        "roleId": None,
        "dataScope": "1",
        "deptIds": deptIds,
        "deptCheckStrictly": deptCheckStrictly,
    }
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()


@Api.urlencoded
@allure.step("角色部门树-lst_role_dept_tree")
def lst_role_dept_tree(roleId="", **kwargs):
    req_url = f"/dev-api/system/role/deptTree/{roleId}"
    req_method = "GET"
    req_params = {}
    auto_fill = False
    rsp_check = {"msg": "操作成功", "code": 200}
    return locals()
