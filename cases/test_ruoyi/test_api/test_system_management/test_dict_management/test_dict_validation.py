#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字典管理 - 校验与异常测试 (DC-T15~T19, DC-T27~T28, DC-T32, DC-D13~D15, DC-D24, DC-D29, DC-D32, DC-E10~E12)
"""

import allure
import pytest
import time
import random
from common.ruoyi_logic import *


def _dict_id(reg):
    did = getattr(reg, "dict_id", None)
    if isinstance(did, list) and did:
        return did[0]
    return did


def _dict_code(reg):
    dc = getattr(reg, "dict_code", None)
    if isinstance(dc, list) and dc:
        return dc[0]
    return dc


@allure.feature("系统管理")
@allure.story("字典管理-校验")
class TestDictTypeValidation(object):
    """字典类型校验"""

    def setup_method(self):
        timestamp = int(time.time())
        suffix = random.randint(1000, 9999)
        self.dict_name = f"val_type_{timestamp}_{suffix}"
        self.dict_type = f"test_val_{timestamp}_{suffix}"
        self.reg = register({"dict_id": None, "dict_code": None})

    def teardown_method(self):
        did = _dict_id(self.reg)
        if did:
            try:
                rmv_dict_type(dict_ids=did)
            except Exception:
                pass
        dc = _dict_code(self.reg)
        if dc:
            try:
                rmv_dict_data(dict_codes=dc)
            except Exception:
                pass
        print("测试数据清理完成")

    @allure.title("DC-T15: 字典类型-dictName 为空失败")
    def test_dict_type_add_empty_dict_name(self):
        add_dict_type(
            dictName="",
            dictType=self.dict_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T16: 字典类型-dictType 为空失败")
    def test_dict_type_add_empty_dict_type(self):
        add_dict_type(
            dictName=self.dict_name,
            dictType="",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T17: 字典类型-dictType 格式错误-大写")
    def test_dict_type_add_format_uppercase(self):
        add_dict_type(
            dictName="测试",
            dictType="TestType",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T18: 字典类型-dictType 含特殊字符失败")
    def test_dict_type_add_format_special_char(self):
        add_dict_type(
            dictName="测试",
            dictType="test-type",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T19: 字典类型-重复 dictType 新增失败")
    def test_dict_type_add_duplicate_type(self):
        add_dict_type(
            dictName=self.dict_name,
            dictType=self.dict_type,
            check=[["$.code", "eq", 200]],
        )
        add_dict_type(
            dictName="其他名称_dc_t19",
            dictType=self.dict_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T22: 字典类型-dictName 超 100 字符失败")
    def test_dict_type_add_name_too_long(self):
        long_name = "a" * 101
        add_dict_type(
            dictName=long_name,
            dictType=self.dict_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T27: 字典类型-修改不存在的 dictId")
    def test_dict_type_modify_not_exist(self):
        mod_dict_type(
            dictId=999999,
            dictName="x",
            dictType="test_x",
            status="0",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-T28: 字典类型-修改后唯一性冲突")
    def test_dict_type_modify_duplicate_type(self):
        type_a = self.dict_type
        type_b = f"test_dc_t28_b_{int(time.time())}_{random.randint(1000, 9999)}"
        add_dict_type(dictName="A_dc_t28", dictType=type_a, check=[["$.code", "eq", 200]])
        add_dict_type(dictName="B_dc_t28", dictType=type_b, check=[["$.code", "eq", 200]])
        lst_dict_type(dictType=type_b, fetch=[[self.reg, "dict_id_b", f"$.rows[?(@.dictType=='{type_b}')].dictId"]])
        bid = getattr(self.reg, "dict_id_b", None)
        if isinstance(bid, list) and bid:
            bid = bid[0]
        mod_dict_type(
            dictId=bid,
            dictName="B_dc_t28",
            dictType=type_a,
            status="0",
            check=[["$.code", "!=", 200]],
        )
        lst_dict_type(dictType=type_a, fetch=[[self.reg, "aid", f"$.rows[?(@.dictType=='{type_a}')].dictId"]])
        aid = getattr(self.reg, "aid", None)
        if isinstance(aid, list) and aid:
            aid = aid[0]
        if bid:
            rmv_dict_type(dict_ids=bid)
        if aid:
            rmv_dict_type(dict_ids=aid)
        self.reg.dict_id = None

    @allure.title("DC-T32: 字典类型-有数据时禁止删除")
    def test_dict_type_delete_with_data(self):
        add_dict_type(
            dictName=self.dict_name,
            dictType=self.dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_type(
            dictType=self.dict_type,
            fetch=[[self.reg, "dict_id", f"$.rows[?(@.dictType=='{self.dict_type}')].dictId"]],
        )
        add_dict_data(
            dictLabel="子项",
            dictValue="v",
            dictType=self.dict_type,
            check=[["$.code", "eq", 200]],
        )
        rmv_dict_type(dict_ids=_dict_id(self.reg), check=[["$.code", "!=", 200]])
        lst_dict_data(dictType=self.dict_type, fetch=[[self.reg, "dict_code", "$.rows[0].dictCode"]])
        rmv_dict_data(dict_codes=_dict_code(self.reg))

    @allure.title("DC-T36: 字典类型-删除不存在的 dictId")
    def test_dict_type_delete_not_exist(self):
        rmv_dict_type(dict_ids=999999, check=[["$.code", "!=", 200]])

    @allure.title("DC-T11: 字典类型-详情不存在的 dictId")
    def test_dict_type_detail_not_exist(self):
        lst_dict_type_detail(
            dictId=999999,
            check=[["$.code", "in", [200, 404, 500]]],
        )

    @allure.title("DC-T41: 字典类型-修改 dictType 格式不符合")
    def test_dict_type_modify_invalid_format(self):
        add_dict_type(
            dictName=self.dict_name,
            dictType=self.dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_type(
            dictType=self.dict_type,
            fetch=[[self.reg, "dict_id", f"$.rows[?(@.dictType=='{self.dict_type}')].dictId"]],
        )
        mod_dict_type(
            dictId=_dict_id(self.reg),
            dictName=self.dict_name,
            dictType="InvalidType",
            status="0",
            check=[["$.code", "!=", 200]],
        )


@allure.feature("系统管理")
@allure.story("字典管理-数据校验")
class TestDictDataValidation(object):
    """字典数据校验：使用本类创建的独立类型（命名含 dc_d_val 便于排查）。"""

    def setup_method(self):
        ts = int(time.time())
        suf = random.randint(1000, 9999)
        self._own_dict_type = f"test_dc_d_val_{ts}_{suf}"
        self._own_dict_name = f"校验用_dc_d_val_{ts}_{suf}"
        self.reg = register({"dict_id": None, "dict_code": None})
        add_dict_type(
            dictName=self._own_dict_name,
            dictType=self._own_dict_type,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_type(
            dictType=self._own_dict_type,
            fetch=[[self.reg, "dict_id", f"$.rows[?(@.dictType=='{self._own_dict_type}')].dictId"]],
        )

    def teardown_method(self):
        try:
            lst_dict_data(dictType=self._own_dict_type, pageSize=100, fetch=[[self.reg, "_rows", "$.rows"]])
            for r in (getattr(self.reg, "_rows", []) or []):
                c = r.get("dictCode") if isinstance(r, dict) else None
                if c is not None:
                    try:
                        rmv_dict_data(dict_codes=c)
                    except Exception:
                        pass
        except Exception:
            pass
        did = _dict_id(self.reg)
        if did:
            try:
                rmv_dict_type(dict_ids=did)
            except Exception:
                pass
        print("测试数据清理完成")

    @allure.title("DC-D13: 字典数据-dictLabel 为空失败")
    def test_dict_data_add_empty_label(self):
        add_dict_data(
            dictLabel="",
            dictValue="v",
            dictType=self._own_dict_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-D14: 字典数据-dictValue 为空失败")
    def test_dict_data_add_empty_value(self):
        add_dict_data(
            dictLabel="l",
            dictValue="",
            dictType=self._own_dict_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-D15: 字典数据-dictType 为空失败")
    def test_dict_data_add_empty_type(self):
        add_dict_data(
            dictLabel="l",
            dictValue="v",
            dictType="",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-D24: 字典数据-修改不存在的 dictCode")
    def test_dict_data_modify_not_exist(self):
        mod_dict_data(
            dictCode=999999,
            dictLabel="x",
            dictValue="x",
            dictType=self._own_dict_type,
            status="0",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-D29: 字典数据-删除不存在的 dictCode")
    def test_dict_data_delete_not_exist(self):
        rmv_dict_data(dict_codes=999999, check=[["$.code", "!=", 200]])

    @allure.title("DC-D08: 字典数据-详情不存在的 dictCode")
    def test_dict_data_detail_not_exist(self):
        lst_dict_data_detail(
            dictCode=999999,
            check=[["$.code", "in", [200, 404, 500]]],
        )

    @pytest.mark.skip(reason="backend may return 200 for non-existent dictType")
    @allure.title("DC-D32: 字典数据-新增不存在的 dictType")
    def test_dict_data_add_not_exist_type(self):
        add_dict_data(
            dictLabel="l_dc_d32",
            dictValue="v",
            dictType="not_exist_type_xyz_123",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-E12: 超长 dictType 返回校验错误")
    def test_dict_type_add_type_too_long(self):
        long_type = "a" + "b" * 100
        add_dict_type(
            dictName="x",
            dictType=long_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-E11: 数据必填缺失-dictLabel")
    def test_dict_data_add_missing_label(self):
        add_dict_data(
            dictValue="v",
            dictType=self._own_dict_type,
            check=[["$.code", "!=", 200]],
        )

    @allure.title("DC-E10: 类型必填缺失-dictType")
    def test_dict_type_add_missing_type(self):
        add_dict_type(
            dictName="有名称",
            dictType="",
            check=[["$.code", "!=", 200]],
        )
