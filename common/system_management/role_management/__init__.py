from core.logic import Api


@Api.json
def add_role(roleName="", roleKey="", remark="", **kwargs):
    req_method = "POST"
    req_url = "dev-api/system/role"
    req_json = {
        "roleName": "",
        "roleKey": "",
        "roleSort": 3,
        "status": "0",
        "menuIds": [],
        "deptIds": [],
        "menuCheckStrictly": True,
        "deptCheckStrictly": True,
        "remark": ""
    }
    rsp_check = {
        "msg": "操作成功"
    }
    return locals()


@Api.urlencoded
def lst_role(**kwargs):
    req_method = "GET"
    req_url = "dev-api/system/role/list"
    req_params = {
        "pageNum": 1,
        "pageSize": 10
    }
    rsp_check = {
        "msg": "查询成功"
    }
    return locals()


@Api.json
def rmv_role(roleId=None, **kwargs):
    req_method = "DELETE"
    req_url = f"dev-api/system/role/{roleId}"
    req_json = {}
    rsp_check = {
        "msg": "操作成功"
    }
    fill_req_json = False
    return locals()

