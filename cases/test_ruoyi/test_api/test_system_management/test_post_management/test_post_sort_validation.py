#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 显示顺序验证测试 (TC-D01~TC-D10)
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
class TestPostSortValidation(object):
    """显示顺序 postSort 验证"""

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

    @allure.title("TC-D01: postSort为0")
    def test_sort_zero(self):
        self._gen("TC_D01")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=0,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.postSort", "eq", 0]])

    @allure.title("TC-D02: postSort正整数")
    def test_sort_positive(self):
        self._gen("TC_D02")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=100,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.postSort", "eq", 100]])

    @allure.title("TC-D03: postSort最大值")
    def test_sort_max(self):
        self._gen("TC_D03")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=2147483647,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.postSort", "eq", 2147483647]])

    @allure.title("TC-D04: postSort负数-存储的值应为非负整数")
    def test_sort_negative(self):
        self._gen("TC_D04")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=-1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(
            positionId=_pid(self.reg),
            check=[["$.data.postSort", ">=", 0]],
        )

    @allure.title("TC-D05: postSort空null")
    def test_sort_null(self):
        self._gen("TC_D05")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=None,
            check=[["$.code", "eq", 500], ["$.msg", "include", "显示顺序不能为空"]],
        )

    @allure.title("TC-D06: postSort小数-存储的值应为整数")
    def test_sort_decimal(self):
        self._gen("TC_D06")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1.5,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(
            positionId=_pid(self.reg),
            check=[["$.data.postSort", "eq", 1]],
        )

    @allure.title("TC-D07: postSort字符串")
    def test_sort_string(self):
        self._gen("TC_D07")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort="1",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.postSort", "eq", 1]])

    @allure.title("TC-D08: 列表按postSort排序")
    def test_list_sorted_by_sort(self):
        lst_position(pageNum=1, pageSize=20, check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-D09: 修改postSort后排序")
    def test_update_sort_then_list(self):
        self._gen("TC_D09")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=999,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        mod_position(
            positionId=_pid(self.reg),
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.postSort", "eq", 1]])

    @allure.title("TC-D10: postSort相同多岗位")
    def test_same_sort_multiple(self):
        ts = int(time.time())
        name1 = f"TC_D10_s1_{ts}_{random.randint(100, 999)}"
        name2 = f"TC_D10_s2_{ts}_{random.randint(100, 999)}"
        code1 = f"TC_D10_sc1_{ts}_{random.randint(100, 999)}"
        code2 = f"TC_D10_sc2_{ts}_{random.randint(100, 999)}"
        add_position(positionName=name1, positionCode=code1, postSort=10, check=[["$.code", "eq", 200]])
        add_position(positionName=name2, positionCode=code2, postSort=10, check=[["$.code", "eq", 200]])
        lst_position(postName=name1[:10], check=[["$.code", "eq", 200], ["$.rows", "exist", True]])
        reg = register({"position_id": None, "position_id2": None})
        lst_position(postName=name1, fetch=[[reg, "position_id", f"$.rows[?(@.postName=='{name1}')].postId"]])
        lst_position(postName=name2, fetch=[[reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        pid1 = reg.position_id[0] if isinstance(reg.position_id, list) else reg.position_id
        pid2 = reg.position_id2[0] if isinstance(reg.position_id2, list) else reg.position_id2
        if pid1:
            rmv_position(positionId=pid1)
        if pid2:
            rmv_position(positionId=pid2)
        self.reg.position_id = None
