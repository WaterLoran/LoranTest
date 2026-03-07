#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 组合筛选测试 (TC-J01~TC-J08)
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
class TestPostFilter(object):
    """列表组合筛选"""

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

    @allure.title("TC-J01: 仅名称")
    def test_filter_name_only(self):
        self._gen("TC_J01")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-J02: 仅编码")
    def test_filter_code_only(self):
        self._gen("TC_J02")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postCode=self.post_code,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postCode=='{self.post_code}')].postId"]],
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-J03: 仅状态")
    def test_filter_status_only(self):
        lst_position(status="0", check=[["$.code", "eq", 200]])
        lst_position(status="1", check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-J04: 名称加状态")
    def test_filter_name_and_status(self):
        self._gen("TC_J04")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position(
            postName=self.post_name,
            status="0",
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-J05: 编码加状态")
    def test_filter_code_and_status(self):
        self._gen("TC_J05")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="1",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position(
            postCode=self.post_code,
            status="1",
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-J06: 名称加编码")
    def test_filter_name_and_code(self):
        self._gen("TC_J06")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position(
            postName=self.post_name,
            postCode=self.post_code,
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-J07: 名称编码状态全选")
    def test_filter_all(self):
        self._gen("TC_J07")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position(
            postName=self.post_name,
            postCode=self.post_code,
            status="0",
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-J08: 条件无匹配结果")
    def test_filter_no_match(self):
        lst_position(
            postName="TC_J08_不可能存在的岗位名称_xyz_99999",
            postCode="TC_J08_不可能存在的编码_xyz_99999",
            check=[["$.code", "eq", 200], ["$.total", "eq", 0]],
        )
        self.reg.position_id = None
