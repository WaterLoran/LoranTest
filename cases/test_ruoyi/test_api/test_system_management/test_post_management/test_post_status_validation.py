#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 状态验证测试 (TC-E01~TC-E08)
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
class TestPostStatusValidation(object):
    """状态 status 验证"""

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

    @allure.title("TC-E01: status为0正常")
    def test_status_normal(self):
        self._gen("TC_E01")
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
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.status", "eq", "0"]])
        lst_position(status="0", check=[["$.code", "eq", 200]])

    @allure.title("TC-E02: status为1停用")
    def test_status_disabled(self):
        self._gen("TC_E02")
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
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.status", "eq", "1"]])
        lst_position(status="1", check=[["$.code", "eq", 200]])

    @allure.title("TC-E03: status无效值2")
    def test_status_invalid(self):
        self._gen("TC_E03")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="2",
            check=[["$.code", "in", [200, 500]]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )

    @allure.title("TC-E04: status空字符串")
    def test_status_empty(self):
        self._gen("TC_E04")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="",
            check=[["$.code", "eq", 500], ["$.msg", "include", "status"]],
        )
        self.reg.position_id = None

    @allure.title("TC-E05: status非数字")
    def test_status_non_numeric(self):
        self._gen("TC_E05")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="正常",
            check=[["$.code", "eq", 500]],
        )

    @allure.title("TC-E06: 正常改停用")
    def test_normal_to_disabled(self):
        self._gen("TC_E06")
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
        mod_position(
            positionId=_pid(self.reg),
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="1",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.status", "eq", "1"]])

    @allure.title("TC-E07: 停用改正常")
    def test_disabled_to_normal(self):
        self._gen("TC_E07")
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
        mod_position(
            positionId=_pid(self.reg),
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.status", "eq", "0"]])

    @allure.title("TC-E08: 下拉选项含状态")
    def test_optionselect_has_status(self):
        optionselect_position(check=[["$.code", "eq", 200], ["$.data", "exist", True]])
        self.reg.position_id = None
