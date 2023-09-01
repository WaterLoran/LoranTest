from core.logic import Api


@Api.json
def add_user(userName="", nickName="", password="", **kwargs):
    req_method = "POST"
    req_url = "dev-api/system/user"
    req_json = {
        "userName": "",
        "nickName": "",
        "password": "",
        "status": "0",
        "postIds": [],
        "roleIds": []
    }
    rsp_check = {
        "msg": "操作成功"
    }
    return locals()


@Api.urlencoded
def lst_user(**kwargs):
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


@Api.json
def rmv_user(userId=None, **kwargs):
    req_method = "DELETE"
    req_url = f"dev-api/system/user/{userId}"
    req_json = {}
    rsp_check = {
        "msg": "操作成功"
    }
    fill_req_json = False
    return locals()

