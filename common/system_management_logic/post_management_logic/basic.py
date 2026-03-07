from core.logic import *
import allure


@Api.json
@allure.step("添加岗位-add_position")
def add_position(positionName="", positionCode="", postSort=0, status="0", remark="", **kwargs):
    req_url = "/dev-api/system/post"
    req_method = "POST"
    req_json = {
        "postName": "",      # 岗位名称
        "postCode": "",      # 岗位编码
        "postSort": 0,       # 显示顺序
        "status": "0",       # 状态（0正常 1停用）
        "remark": ""         # 备注
    }
    req_field = {
        "req_json_all": {"jsonpath": "$"},
        "positionName": {"jsonpath": "$.postName"},
        "positionCode": {"jsonpath": "$.postCode"},
        "postSort": {"jsonpath": "$.postSort"},
        "status": {"jsonpath": "$.status"},
        "remark": {"jsonpath": "$.remark"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"}  # 岗位ID
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    
    # Restore机制：从响应中提取岗位ID，用于后续清理
    # 注意：根据框架模式，API调用返回bool类型，restore参数需要特殊处理
    # 这里使用查询方式获取岗位ID
    restore = {
        "rmv_position": {
            "positionId": f"$.rows[?(@.postName=='{positionName}')].postId"
        }
    }
    
    return locals()


@Api.urlencoded
@allure.step("查看岗位列表-lst_position")
def lst_position(postName="", postCode="", status="", pageNum=1, pageSize=10, **kwargs):
    req_url = "/dev-api/system/post/list"
    req_method = "GET"
    req_params = {
        "pageNum": 1,      # 页码
        "pageSize": 10,    # 每页大小
        "postName": "",    # 岗位名称
        "postCode": "",    # 岗位编码
        "status": ""       # 状态
    }
    req_field = {
        "postName": {"jsonpath": "$.postName"},
        "postCode": {"jsonpath": "$.postCode"},
        "status": {"jsonpath": "$.status"},
        "pageNum": {"jsonpath": "$.pageNum"},
        "pageSize": {"jsonpath": "$.pageSize"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "rows": {"jsonpath": "$.rows"},      # 岗位列表
        "total": {"jsonpath": "$.total"},    # 总记录数
    }
    rsp_check = {
        "code": 200,
    }
    
    return locals()


@Api.urlencoded
@allure.step("查看岗位详情-lst_position_detail")
def lst_position_detail(positionId="", **kwargs):
    req_url = f"/dev-api/system/post/{positionId}"
    req_method = "GET"
    req_params = {}
    auto_fill = False
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},  # 岗位详情
    }
    rsp_check = {
        "code": 200,
    }
    
    return locals()


@Api.json
@allure.step("修改岗位-mod_position")
def mod_position(positionId="", positionName="", positionCode="", postSort=0, status="0", remark="", **kwargs):
    req_url = "/dev-api/system/post"
    req_method = "PUT"
    req_json = {
        "postId": "",        # 岗位ID
        "postName": "",      # 岗位名称
        "postCode": "",      # 岗位编码
        "postSort": 0,       # 显示顺序
        "status": "0",       # 状态（0正常 1停用）
        "remark": ""         # 备注
    }
    req_field = {
        "req_json_all": {"jsonpath": "$"},
        "positionId": {"jsonpath": "$.postId"},
        "positionName": {"jsonpath": "$.postName"},
        "positionCode": {"jsonpath": "$.postCode"},
        "postSort": {"jsonpath": "$.postSort"},
        "status": {"jsonpath": "$.status"},
        "remark": {"jsonpath": "$.remark"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"}
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    
    # Restore机制：修改操作也需要清理
    restore = {
        "rmv_position": {
            "positionId": positionId  # 使用传入的岗位ID
        }
    }
    
    return locals()


@Api.json
@allure.step("删除岗位-rmv_position")
def rmv_position(positionId="", **kwargs):
    req_url = f"/dev-api/system/post/{positionId}"
    req_method = "DELETE"
    req_json = {}
    auto_fill = False
    rsp_field = {
        "msg": {"jsonpath": "$.msg"}
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    
    return locals()


@Api.urlencoded
@allure.step("导出岗位-export_position")
def export_position(postName="", postCode="", status="", **kwargs):
    req_url = "/dev-api/system/post/export"
    req_method = "POST"
    req_params = {
        "postName": "",    # 岗位名称
        "postCode": "",    # 岗位编码
        "status": ""       # 状态
    }
    req_field = {
        "postName": {"jsonpath": "$.postName"},
        "postCode": {"jsonpath": "$.postCode"},
        "status": {"jsonpath": "$.status"},
    }
    rsp_check = {}
    return locals()


@Api.urlencoded
@allure.step("获取岗位下拉选项-optionselect_position")
def optionselect_position(**kwargs):
    req_url = "/dev-api/system/post/optionselect"
    req_method = "GET"
    req_params = {}
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},  # 岗位选项列表
    }
    rsp_check = {
        "code": 200,
    }
    
    return locals()