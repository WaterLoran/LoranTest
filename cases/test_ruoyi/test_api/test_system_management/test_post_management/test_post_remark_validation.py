#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 备注验证测试 (TC-F01~TC-F08)
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
class TestPostRemarkValidation(object):
    """备注 remark 验证"""

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

    @allure.title("TC-F01: 备注为空")
    def test_remark_empty(self):
        self._gen("TC_F01")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark="",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.remark", "in", ["", None]]])

    @allure.title("TC-F02: 备注可选不传")
    def test_remark_optional(self):
        self._gen("TC_F02")
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
        lst_position_detail(positionId=_pid(self.reg), check=[["$.code", "eq", 200]])

    @allure.title("TC-F03: 备注500字符边界")
    def test_remark_500_chars(self):
        self._gen("TC_F03")
        remark_500 = "备" * 500
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark=remark_500,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.remark", "eq", remark_500]])

    @allure.title("TC-F04: 备注501字符超长")
    def test_remark_501_chars(self):
        self._gen("TC_F04")
        remark_501 = "x" * 501
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark=remark_501,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("TC-F05: 备注特殊字符")
    def test_remark_special(self):
        self._gen("TC_F05")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark="备注!@#$%",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.remark", "eq", "备注!@#$%"]])

    @allure.title("TC-F06: 备注中文")
    def test_remark_chinese(self):
        self._gen("TC_F06")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark="这是中文备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.remark", "eq", "这是中文备注"]])

    @allure.title("TC-F07: 备注换行")
    def test_remark_newline(self):
        self._gen("TC_F07")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark="第一行\n第二行",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.remark", "eq", "第一行\n第二行"]])

    @allure.title("TC-F08: 备注null")
    def test_remark_null(self):
        self._gen("TC_F08")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            remark=None,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.code", "eq", 200]])
