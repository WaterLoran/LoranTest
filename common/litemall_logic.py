from core.logic import Api


@Api.json
def add_goods(goodsSn="", name="", **kwargs):
    req_method = "POST"
    url = "admin/goods/create"
    body_data = {
        "goods": {
            "picUrl": "",
            "gallery": [],
            "isHot": False,
            "isNew": True,
            "isOnSale": True,
            "goodsSn": "9001",
            "name": None
        },
        "specifications": [{
            "specification": "规格",
            "value": "标准",
            "picUrl": ""
        }],
        "products": [{
            "id": 0,
            "specifications": ["标准"],
            "price": "66",
            "number": "66",
            "url": ""
        }],
        "attributes": []
    }
    return req_method, url, body_data


@Api.json
def rmv_goods(id="", **kwargs):
    req_method = "POST"
    url = "admin/goods/delete"
    body_data = {"id": None}
    return req_method, url, body_data


@Api.json
def lst_goods(name="", **kwargs):
    req_method = "GET"
    url = "admin/goods/list"
    body_data = {
        "name": "",
        "order": "desc",
        "sort": "add_time"
    }
    return req_method, url, body_data

@Api.json
def dtl_goods(id="", **kwargs):
    req_method = "GET"
    url = "admin/goods/detail"
    body_data = {"id": None}
    return req_method, url, body_data
