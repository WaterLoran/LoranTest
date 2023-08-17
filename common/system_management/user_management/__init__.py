from core.logic import Api

@Api.urlencoded
def lst_system_user():
    req_method = "GET"
    req_url = "dev-api/system/user/list"
    req_params = {
        "pageNum": 1,
        "pageSize": 10
    }
    rsp_check = {
        "msg": "查询成功"
    }
    return locals()

