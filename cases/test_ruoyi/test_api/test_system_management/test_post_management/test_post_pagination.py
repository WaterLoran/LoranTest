#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 分页测试 (TC-I01~TC-I10)
"""

import allure
import time
import random
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("岗位管理")
class TestPostPagination(object):
    """列表分页"""

    def setup_method(self):
        self.reg = register({"position_id": None})

    @allure.title("TC-I01: 默认分页")
    def test_default_pagination(self):
        lst_position(
            pageNum=1,
            pageSize=10,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True], ["$.total", ">=", 0]],
        )

    @allure.title("TC-I02: 自定义pageSize")
    def test_custom_page_size(self):
        lst_position(
            pageNum=1,
            pageSize=5,
            check=[["$.code", "eq", 200], ["$.total", ">=", 0]],
        )
        self.reg.position_id = None

    @allure.title("TC-I03: 页码超出总页")
    def test_page_beyond_total(self):
        lst_position(pageNum=1, pageSize=10, fetch=[[self.reg, "total", "$.total"]])
        total = self.reg.total
        big_page = (total // 10) + 10 if total else 10
        lst_position(
            pageNum=big_page,
            pageSize=10,
            check=[["$.code", "eq", 200], ["$.total", "eq", total]],
        )
        self.reg.position_id = None

    @allure.title("TC-I04: 页码0或负")
    def test_page_zero_or_negative(self):
        lst_position(pageNum=0, pageSize=10, check=[["$.code", "eq", 200]])
        lst_position(pageNum=-1, pageSize=10, check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-I05: pageSize为1")
    def test_page_size_one(self):
        lst_position(
            pageNum=1,
            pageSize=1,
            check=[["$.code", "eq", 200], ["$.total", ">=", 0]],
        )
        self.reg.position_id = None

    @allure.title("TC-I06: pageSize极大")
    def test_page_size_large(self):
        lst_position(
            pageNum=1,
            pageSize=99999,
            check=[["$.code", "eq", 200]],
        )
        self.reg.position_id = None

    @allure.title("TC-I07: total总数正确")
    def test_total_consistent(self):
        lst_position(pageNum=1, pageSize=1, fetch=[[self.reg, "total", "$.total"]])
        total = self.reg.total
        lst_position(check=[["$.total", "eq", total]])
        self.reg.position_id = None

    @allure.title("TC-I08: 多页数据不重复")
    def test_multi_page_no_duplicate(self):
        lst_position(pageNum=1, pageSize=2, fetch=[[self.reg, "page1_ids", "$.rows[*].postId"]])
        lst_position(pageNum=2, pageSize=2, fetch=[[self.reg, "page2_ids", "$.rows[*].postId"]])
        ids1 = self.reg.page1_ids
        ids2 = self.reg.page2_ids
        if ids1 is not None and ids2 is not None:
            ids1 = ids1 if isinstance(ids1, list) else [ids1]
            ids2 = ids2 if isinstance(ids2, list) else [ids2]
            for i in ids1:
                assert i not in ids2
        self.reg.position_id = None

    @allure.title("TC-I09: pageSize为0")
    def test_page_size_zero(self):
        lst_position(pageNum=1, pageSize=0, check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-I10: 首页末页一致性")
    def test_first_last_page_consistency(self):
        lst_position(pageNum=1, pageSize=10, fetch=[[self.reg, "total", "$.total"]])
        total = self.reg.total
        if total > 0:
            last_page = (total + 9) // 10
            lst_position(
                pageNum=last_page,
                pageSize=10,
                check=[["$.code", "eq", 200], ["$.total", "eq", total]],
            )
        self.reg.position_id = None
