"""
部门管理模块 API 封装
封装完成后的 Logic 文件，对应 RuoYi SysDeptController。
"""
from core.logic import *
import allure


@Api.json
@allure.step("添加部门-add_dept")
def add_dept(
    parentId=100,
    deptName="",
    orderNum=0,
    leader="",
    phone="",
    email="",
    status="0",
    **kwargs,
):
    req_url = "/dev-api/system/dept"
    req_method = "POST"
    req_json = {
        "parentId": 100,
        "deptName": "",
        "orderNum": 0,
        "leader": "",
        "phone": "",
        "email": "",
        "status": "0",
    }
    req_field = {
        "parentId": {"jsonpath": "$.parentId"},
        "deptName": {"jsonpath": "$.deptName"},
        "orderNum": {"jsonpath": "$.orderNum"},
        "leader": {"jsonpath": "$.leader"},
        "phone": {"jsonpath": "$.phone"},
        "email": {"jsonpath": "$.email"},
        "status": {"jsonpath": "$.status"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    # 部门列表为树形，用递归 jsonpath 查找新建部门 ID
    restore = {
        "rmv_dept": {
            "deptId": f"$..[?(@.deptName=='{deptName}')].deptId"
        }
    }
    return locals()


@Api.urlencoded
@allure.step("查看部门列表-lst_dept")
def lst_dept(deptName="", status="", **kwargs):
    req_url = "/dev-api/system/dept/list"
    req_method = "GET"
    req_params = {
        "deptName": "",
        "status": "",
    }
    req_field = {
        "deptName": {"jsonpath": "$.deptName"},
        "status": {"jsonpath": "$.status"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()


@Api.urlencoded
@allure.step("查看部门详情-lst_dept_detail")
def lst_dept_detail(deptId="", **kwargs):
    req_url = f"/dev-api/system/dept/{deptId}"
    req_method = "GET"
    req_params = {}
    auto_fill = False
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()


@Api.urlencoded
@allure.step("查看部门列表排除节点-lst_dept_exclude")
def lst_dept_exclude(deptId="", **kwargs):
    req_url = f"/dev-api/system/dept/list/exclude/{deptId}"
    req_method = "GET"
    req_params = {}
    auto_fill = False
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()


@Api.json
@allure.step("修改部门-mod_dept")
def mod_dept(
    deptId="",
    parentId=100,
    deptName="",
    orderNum=0,
    leader="",
    phone="",
    email="",
    status="0",
    **kwargs,
):
    req_url = "/dev-api/system/dept"
    req_method = "PUT"
    req_json = {
        "deptId": "",
        "parentId": 100,
        "deptName": "",
        "orderNum": 0,
        "leader": "",
        "phone": "",
        "email": "",
        "status": "0",
    }
    req_field = {
        "deptId": {"jsonpath": "$.deptId"},
        "parentId": {"jsonpath": "$.parentId"},
        "deptName": {"jsonpath": "$.deptName"},
        "orderNum": {"jsonpath": "$.orderNum"},
        "leader": {"jsonpath": "$.leader"},
        "phone": {"jsonpath": "$.phone"},
        "email": {"jsonpath": "$.email"},
        "status": {"jsonpath": "$.status"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()


@Api.json
@allure.step("删除部门-rmv_dept")
def rmv_dept(deptId="", **kwargs):
    req_url = f"/dev-api/system/dept/{deptId}"
    req_method = "DELETE"
    req_json = {}
    auto_fill = False
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()
