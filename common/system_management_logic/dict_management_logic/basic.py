# coding: utf-8
"""字典管理 Logic：字典类型与字典数据 CRUD、列表、导出、缓存、optionselect、按类型查数据。"""
from core.logic import *
import allure


def _norm_ids(ids):
    """将单 id 或 list 转为路径用的逗号分隔字符串。"""
    if ids is None:
        return ""
    if isinstance(ids, list):
        return ",".join(str(x) for x in ids)
    return str(ids)


# ---------- 字典类型 ----------

@Api.urlencoded
@allure.step("字典类型列表-lst_dict_type")
def lst_dict_type(dictName="", dictType="", status="", pageNum=1, pageSize=10, **kwargs):
    req_method = "GET"
    req_url = "/dev-api/system/dict/type/list"
    req_params = {
        "pageNum": 1,
        "pageSize": 10,
        "dictName": "",
        "dictType": "",
        "status": "",
    }
    req_field = {
        "dictName": {"jsonpath": "$.dictName"},
        "dictType": {"jsonpath": "$.dictType"},
        "status": {"jsonpath": "$.status"},
        "pageNum": {"jsonpath": "$.pageNum"},
        "pageSize": {"jsonpath": "$.pageSize"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "rows": {"jsonpath": "$.rows"},
        "total": {"jsonpath": "$.total"},
    }
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("字典类型详情-lst_dict_type_detail")
def lst_dict_type_detail(dictId="", **kwargs):
    req_method = "GET"
    req_url = f"/dev-api/system/dict/type/{dictId}"
    req_params = {}
    auto_fill = False
    rsp_field = {"msg": {"jsonpath": "$.msg"}, "data": {"jsonpath": "$.data"}}
    rsp_check = {"code": 200}
    return locals()


@Api.json
@allure.step("新增字典类型-add_dict_type")
def add_dict_type(dictName="", dictType="", status="0", remark="", **kwargs):
    req_method = "POST"
    req_url = "/dev-api/system/dict/type"
    req_json = {
        "dictName": "",
        "dictType": "",
        "status": "0",
        "remark": "",
    }
    req_field = {
        "dictName": {"jsonpath": "$.dictName"},
        "dictType": {"jsonpath": "$.dictType"},
        "status": {"jsonpath": "$.status"},
        "remark": {"jsonpath": "$.remark"},
    }
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200, "msg": "操作成功"}
    return locals()


@Api.json
@allure.step("修改字典类型-mod_dict_type")
def mod_dict_type(dictId="", dictName="", dictType="", status="0", remark="", **kwargs):
    req_method = "PUT"
    req_url = "/dev-api/system/dict/type"
    req_json = {
        "dictId": None,
        "dictName": "",
        "dictType": "",
        "status": "0",
        "remark": "",
    }
    req_field = {
        "dictId": {"jsonpath": "$.dictId"},
        "dictName": {"jsonpath": "$.dictName"},
        "dictType": {"jsonpath": "$.dictType"},
        "status": {"jsonpath": "$.status"},
        "remark": {"jsonpath": "$.remark"},
    }
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200, "msg": "操作成功"}
    return locals()


@Api.urlencoded
@allure.step("删除字典类型-rmv_dict_type")
def rmv_dict_type(dict_ids=None, **kwargs):
    req_method = "DELETE"
    req_url = f"/dev-api/system/dict/type/{_norm_ids(dict_ids)}"
    req_params = {}
    auto_fill = False
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("导出字典类型-export_dict_type")
def export_dict_type(dictName="", dictType="", status="", **kwargs):
    req_method = "POST"
    req_url = "/dev-api/system/dict/type/export"
    req_params = {
        "dictName": "",
        "dictType": "",
        "status": "",
    }
    req_field = {
        "dictName": {"jsonpath": "$.dictName"},
        "dictType": {"jsonpath": "$.dictType"},
        "status": {"jsonpath": "$.status"},
    }
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("刷新字典缓存-refresh_dict_cache")
def refresh_dict_cache(**kwargs):
    req_method = "DELETE"
    req_url = "/dev-api/system/dict/type/refreshCache"
    req_params = {}
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("字典类型下拉-optionselect_dict_type")
def optionselect_dict_type(**kwargs):
    req_method = "GET"
    req_url = "/dev-api/system/dict/type/optionselect"
    req_params = {}
    rsp_field = {"msg": {"jsonpath": "$.msg"}, "data": {"jsonpath": "$.data"}}
    rsp_check = {"code": 200}
    return locals()


# ---------- 字典数据 ----------

@Api.urlencoded
@allure.step("字典数据列表-lst_dict_data")
def lst_dict_data(dictType="", dictLabel="", status="", pageNum=1, pageSize=10, **kwargs):
    req_method = "GET"
    req_url = "/dev-api/system/dict/data/list"
    req_params = {
        "pageNum": 1,
        "pageSize": 10,
        "dictType": "",
        "dictLabel": "",
        "status": "",
    }
    req_field = {
        "dictType": {"jsonpath": "$.dictType"},
        "dictLabel": {"jsonpath": "$.dictLabel"},
        "status": {"jsonpath": "$.status"},
        "pageNum": {"jsonpath": "$.pageNum"},
        "pageSize": {"jsonpath": "$.pageSize"},
    }
    rsp_field = {
        "msg": {"jsonpath": "$.msg"},
        "rows": {"jsonpath": "$.rows"},
        "total": {"jsonpath": "$.total"},
    }
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("字典数据详情-lst_dict_data_detail")
def lst_dict_data_detail(dictCode="", **kwargs):
    req_method = "GET"
    req_url = f"/dev-api/system/dict/data/{dictCode}"
    req_params = {}
    auto_fill = False
    rsp_field = {"msg": {"jsonpath": "$.msg"}, "data": {"jsonpath": "$.data"}}
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("按类型查字典数据-lst_dict_data_by_type")
def lst_dict_data_by_type(dictType="", **kwargs):
    req_method = "GET"
    req_url = f"/dev-api/system/dict/data/type/{dictType}"
    req_params = {}
    auto_fill = False
    rsp_field = {"msg": {"jsonpath": "$.msg"}, "data": {"jsonpath": "$.data"}}
    rsp_check = {"code": 200}
    return locals()


@Api.json
@allure.step("新增字典数据-add_dict_data")
def add_dict_data(
    dictLabel="",
    dictValue="",
    dictType="",
    dictSort=0,
    cssClass="",
    listClass="",
    isDefault="N",
    status="0",
    remark="",
    **kwargs,
):
    req_method = "POST"
    req_url = "/dev-api/system/dict/data"
    req_json = {
        "dictSort": 0,
        "dictLabel": "",
        "dictValue": "",
        "dictType": "",
        "cssClass": "",
        "listClass": "",
        "isDefault": "N",
        "status": "0",
        "remark": "",
    }
    req_field = {
        "dictLabel": {"jsonpath": "$.dictLabel"},
        "dictValue": {"jsonpath": "$.dictValue"},
        "dictType": {"jsonpath": "$.dictType"},
        "dictSort": {"jsonpath": "$.dictSort"},
        "cssClass": {"jsonpath": "$.cssClass"},
        "listClass": {"jsonpath": "$.listClass"},
        "isDefault": {"jsonpath": "$.isDefault"},
        "status": {"jsonpath": "$.status"},
        "remark": {"jsonpath": "$.remark"},
    }
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200, "msg": "操作成功"}
    return locals()


@Api.json
@allure.step("修改字典数据-mod_dict_data")
def mod_dict_data(
    dictCode="",
    dictLabel="",
    dictValue="",
    dictType="",
    dictSort=0,
    cssClass="",
    listClass="",
    isDefault="N",
    status="0",
    remark="",
    **kwargs,
):
    req_method = "PUT"
    req_url = "/dev-api/system/dict/data"
    req_json = {
        "dictCode": None,
        "dictSort": 0,
        "dictLabel": "",
        "dictValue": "",
        "dictType": "",
        "cssClass": "",
        "listClass": "",
        "isDefault": "N",
        "status": "0",
        "remark": "",
    }
    req_field = {
        "dictCode": {"jsonpath": "$.dictCode"},
        "dictLabel": {"jsonpath": "$.dictLabel"},
        "dictValue": {"jsonpath": "$.dictValue"},
        "dictType": {"jsonpath": "$.dictType"},
        "dictSort": {"jsonpath": "$.dictSort"},
        "cssClass": {"jsonpath": "$.cssClass"},
        "listClass": {"jsonpath": "$.listClass"},
        "isDefault": {"jsonpath": "$.isDefault"},
        "status": {"jsonpath": "$.status"},
        "remark": {"jsonpath": "$.remark"},
    }
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200, "msg": "操作成功"}
    return locals()


@Api.urlencoded
@allure.step("删除字典数据-rmv_dict_data")
def rmv_dict_data(dict_codes=None, **kwargs):
    req_method = "DELETE"
    req_url = f"/dev-api/system/dict/data/{_norm_ids(dict_codes)}"
    req_params = {}
    auto_fill = False
    rsp_field = {"msg": {"jsonpath": "$.msg"}}
    rsp_check = {"code": 200}
    return locals()


@Api.urlencoded
@allure.step("导出字典数据-export_dict_data")
def export_dict_data(dictType="", dictLabel="", status="", **kwargs):
    req_method = "POST"
    req_url = "/dev-api/system/dict/data/export"
    req_params = {
        "dictType": "",
        "dictLabel": "",
        "status": "",
    }
    req_field = {
        "dictType": {"jsonpath": "$.dictType"},
        "dictLabel": {"jsonpath": "$.dictLabel"},
        "status": {"jsonpath": "$.status"},
    }
    rsp_check = {"code": 200}
    return locals()
