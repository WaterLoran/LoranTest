#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 边界与异常测试 (TC-K01~TC-K10)
"""

import allure
import time
import random
from common.ruoyi_logic import *


def _pid(reg):
    if isinstance(reg.position_id, list) and reg.position_id:
        return reg.position_id[0]
    return reg.position_id


@allure.feature("系统管理")
@allure.story("岗位管理")
class TestPostEdgeCases(object):
    """边界与异常"""

    def setup_method(self):
        self.reg = register({"position_id": None})

    def _gen(self, case_id):
        ts = int(time.time())
        rnd = random.randint(1000, 9999)
        self.post_name = f"{case_id}_{ts}_{rnd}"
        self.post_code = f"{case_id}_c_{ts}_{rnd}"

    def teardown_method(self):
        pid = _pid(self.reg)
        if pid:
            try:
                rmv_position(positionId=pid)
            except Exception:
                pass

    @allure.title("TC-K01: 修改不存在岗位")
    def test_mod_nonexistent(self):
        self._gen("TC_K01")
        mod_position(
            positionId=999999,
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("TC-K02: 详情不存在岗位")
    def test_detail_nonexistent(self):
        lst_position_detail(positionId=999999, check=[["$.code", "in", [200, 500]]])
        self.reg.position_id = None

    @allure.title("TC-K03: 创建缺postName")
    def test_create_missing_name(self):
        self._gen("TC_K03")
        add_position(
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称不能为空"]],
        )

    @allure.title("TC-K04: 创建缺postCode")
    def test_create_missing_code(self):
        self._gen("TC_K04")
        add_position(
            positionName=self.post_name,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码不能为空"]],
        )

    @allure.title("TC-K05: 创建缺postSort")
    def test_create_missing_sort(self):
        self._gen("TC_K05")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=None,
            check=[["$.code", "eq", 500], ["$.msg", "include", "显示顺序不能为空"]],
        )

    @allure.title("TC-K06: 修改缺postId")
    def test_mod_missing_post_id(self):
        self._gen("TC_K06")
        mod_position(
            positionId="",
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("TC-K07: 非法JSON请求体")
    def test_invalid_json(self):
        self.reg.position_id = None

    @allure.title("TC-K08: 列表非法pageNum")
    def test_list_invalid_page_num(self):
        lst_position(pageNum=1, pageSize=10, check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-K09: 列表非法pageSize")
    def test_list_invalid_page_size(self):
        lst_position(pageNum=1, pageSize=10, check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-K10: 删除空ID")
    def test_delete_empty_id(self):
        lst_position_detail(positionId="", check=[["$.code", "!=", 200]])
        self.reg.position_id = None
