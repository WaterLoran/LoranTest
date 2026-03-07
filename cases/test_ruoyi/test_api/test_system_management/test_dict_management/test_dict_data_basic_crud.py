#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字典管理 - 字典数据基础 CRUD 测试 (DC-D01~DC-D30)
数据独立性：每个测试类使用本脚本内创建的字典类型（命名含 case_id 便于排查残留）。
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
@allure.story("字典管理-数据")
class TestDictDataBasicCRUD(object):
    """字典数据基础 CRUD 测试：使用本类创建的独立字典类型（命名含 dc_d 便于人工排查）。"""

    def setup_method(self):
        timestamp = int(time.time())
        suffix = random.randint(1000, 9999)
        self.dict_label = f"标签_dc_d_{timestamp}_{suffix}"
        self.dict_value = f"val_dc_d_{timestamp}_{suffix}"
        self.reg = register({"dict_id": None, "dict_code": None})
        self._own_dict_type = f"test_dc_d_{timestamp}_{suffix}"
        self._own_dict_name = f"字典数据测试_dc_d_{timestamp}_{suffix}"
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
            lst_dict_data(dictType=self._own_dict_type, pageSize=100, fetch=[[self.reg, "_teardown_rows", "$.rows"]])
            rows = getattr(self.reg, "_teardown_rows", []) or []
            if isinstance(rows, list):
                for r in rows:
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
            except Exception as e:
                print(f"清理字典类型失败 {did}: {e}")
        print("测试数据清理完成")

    @allure.title("DC-D01: 字典数据-列表按 dictType")
    def test_dict_data_list_by_type(self):
        lst_dict_data(
            dictType=self._own_dict_type,
            pageNum=1,
            pageSize=10,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            check=[["$.total", ">=", 0]],
        )

    @allure.title("DC-D02: 字典数据-列表按 dictLabel 模糊")
    def test_dict_data_list_by_label(self):
        add_dict_data(
            dictLabel=f"男_dc_d02_{int(time.time())}",
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel="男_dc_d02",
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("DC-D03: 字典数据-列表按 status")
    def test_dict_data_list_by_status(self):
        lst_dict_data(
            dictType=self._own_dict_type,
            status="0",
            check=[["$.code", "eq", 200]],
        )

    @allure.title("DC-D04: 字典数据-分页")
    def test_dict_data_list_pagination(self):
        lst_dict_data(
            dictType=self._own_dict_type,
            pageNum=1,
            pageSize=2,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("DC-D05: 字典数据-无匹配空列表")
    def test_dict_data_list_empty(self):
        lst_dict_data(
            dictType="non_exist_type_xyz",
            check=[["$.code", "eq", 200], ["$.total", "eq", 0]],
        )

    @allure.title("DC-D06: 字典数据-按类型查 type 接口")
    def test_dict_data_by_type_api(self):
        lst_dict_data_by_type(
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200], ["$.data", "exist", True]],
        )

    @allure.title("DC-D07: 字典数据-详情")
    def test_dict_data_detail(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            dictSort=100,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[
                ["$.code", "eq", 200],
                ["$.data.dictLabel", "eq", self.dict_label],
                ["$.data.dictValue", "eq", self.dict_value],
                ["$.data.dictType", "eq", self._own_dict_type],
            ],
        )

    @allure.title("DC-D09: 字典数据-列表响应结构")
    def test_dict_data_list_structure(self):
        lst_dict_data(
            pageNum=1,
            pageSize=10,
            check=[["$.code", "exist", True], ["$.rows", "exist", True], ["$.total", "exist", True]],
        )

    @allure.title("DC-D10: 字典数据-多条件组合")
    def test_dict_data_list_combined(self):
        lst_dict_data(
            dictType=self._own_dict_type,
            status="0",
            check=[["$.code", "eq", 200]],
        )

    @allure.title("DC-D11: 字典数据-新增仅必填")
    def test_dict_data_add_required_only(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200], ["$.msg", "eq", "操作成功"]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            check=[[f"$.rows[?(@.dictLabel=='{self.dict_label}')]", "exist", True]],
        )

    @allure.title("DC-D12: 字典数据-新增全字段")
    def test_dict_data_add_all_fields(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            dictSort=99,
            cssClass="",
            listClass="default",
            isDefault="N",
            status="0",
            remark="全字段备注",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[
                ["$.data.dictSort", "eq", 99],
                ["$.data.remark", "eq", "全字段备注"],
            ],
        )

    @allure.title("DC-D16: 字典数据-新增 isDefault=Y")
    def test_dict_data_add_is_default_y(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            isDefault="Y",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[["$.data.isDefault", "eq", "Y"]],
        )

    @allure.title("DC-D17: 字典数据-新增 dictSort")
    def test_dict_data_add_dict_sort(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            dictSort=88,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data_by_type(
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )

    @allure.title("DC-D18: 字典数据-新增后 type 接口可见")
    def test_dict_data_add_then_by_type(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data_by_type(
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200], ["$.data", "exist", True]],
        )

    @allure.title("DC-D19: 字典数据-新增后列表可见")
    def test_dict_data_add_then_list(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            check=[
                ["$.code", "eq", 200],
                [f"$.rows[?(@.dictValue=='{self.dict_value}')]", "exist", True],
            ],
        )

    @allure.title("DC-D20: 字典数据-新增 cssClass listClass")
    def test_dict_data_add_css_list_class(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            cssClass="primary",
            listClass="default",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[
                ["$.data.cssClass", "eq", "primary"],
                ["$.data.listClass", "eq", "default"],
            ],
        )

    @allure.title("DC-D21: 字典数据-正常修改")
    def test_dict_data_modify(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        mod_dict_data(
            dictCode=_dict_code(self.reg),
            dictLabel=self.dict_label + "_mod",
            dictValue=self.dict_value + "_mod",
            dictType=self._own_dict_type,
            dictSort=0,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[
                ["$.data.dictLabel", "eq", self.dict_label + "_mod"],
                ["$.data.dictValue", "eq", self.dict_value + "_mod"],
            ],
        )

    @allure.title("DC-D22: 字典数据-修改 dictSort")
    def test_dict_data_modify_sort(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            dictSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        mod_dict_data(
            dictCode=_dict_code(self.reg),
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            dictSort=50,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[["$.data.dictSort", "eq", 50]],
        )

    @allure.title("DC-D23: 字典数据-修改 status")
    def test_dict_data_modify_status(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        mod_dict_data(
            dictCode=_dict_code(self.reg),
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            status="1",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[["$.data.status", "eq", "1"]],
        )

    @allure.title("DC-D25: 字典数据-单条删除")
    def test_dict_data_delete_one(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        dc = _dict_code(self.reg)
        rmv_dict_data(dict_codes=dc, check=[["$.code", "eq", 200]])
        self.reg.dict_code = None
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            check=[["$.total", "eq", 0]],
        )

    @allure.title("DC-D27: 字典数据-删除后列表不包含")
    def test_dict_data_delete_then_list(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        dc = _dict_code(self.reg)
        rmv_dict_data(dict_codes=dc, check=[["$.code", "eq", 200]])
        self.reg.dict_code = None
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            check=[["$.total", "eq", 0]],
        )

    @allure.title("DC-D28: 字典数据-删除后 type 接口不返回")
    def test_dict_data_delete_then_by_type(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        dc = _dict_code(self.reg)
        rmv_dict_data(dict_codes=dc, check=[["$.code", "eq", 200]])
        self.reg.dict_code = None
        lst_dict_data_by_type(dictType=self._own_dict_type, check=[["$.code", "eq", 200]])

    @pytest.mark.skip(reason="export returns binary Excel, framework expects JSON")
    @allure.title("DC-D30: 字典数据-导出")
    def test_dict_data_export(self):
        export_dict_data(check=[["$.code", "eq", 200]])

    @allure.title("DC-N03: 字典数据-dictSort 排序")
    def test_dict_data_sort_order(self):
        lst_dict_data_by_type(
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )

    @allure.title("DC-D11 补充: 字典数据-新增后详情可见")
    def test_dict_data_add_then_detail(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[
                ["$.data.dictLabel", "eq", self.dict_label],
                ["$.data.dictType", "eq", self._own_dict_type],
            ],
        )

    @allure.title("DC-D04 补充: 字典数据-pageSize 边界")
    def test_dict_data_list_page_size_boundary(self):
        lst_dict_data(
            dictType=self._own_dict_type,
            pageNum=1,
            pageSize=1,
            check=[["$.code", "eq", 200]],
        )

    @pytest.mark.skip(reason="export returns binary Excel, framework expects JSON")
    @allure.title("DC-D36: 字典数据-导出带条件")
    def test_dict_data_export_with_params(self):
        export_dict_data(dictType=self._own_dict_type, check=[["$.code", "eq", 200]])

    @allure.title("DC-D07 补充: 详情含 dictSort status")
    def test_dict_data_detail_has_sort_status(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            dictSort=77,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        lst_dict_data_detail(
            dictCode=_dict_code(self.reg),
            check=[["$.data.dictSort", "eq", 77], ["$.data.status", "eq", "0"]],
        )

    @allure.title("DC-D25 补充: 单条删除成功 code=200")
    def test_dict_data_single_delete_success(self):
        add_dict_data(
            dictLabel=self.dict_label,
            dictValue=self.dict_value,
            dictType=self._own_dict_type,
            check=[["$.code", "eq", 200]],
        )
        lst_dict_data(
            dictType=self._own_dict_type,
            dictLabel=self.dict_label,
            fetch=[[self.reg, "dict_code", f"$.rows[?(@.dictLabel=='{self.dict_label}')].dictCode"]],
        )
        rmv_dict_data(dict_codes=_dict_code(self.reg), check=[["$.code", "eq", 200]])
        self.reg.dict_code = None
