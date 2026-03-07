#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 岗位名称验证测试 (TC-B01~TC-B15)
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
class TestPostNameValidation(object):
    """岗位名称验证"""

    def _code(self, case_id):
        return f"{case_id}_c_{int(time.time())}_{random.randint(1000, 9999)}"

    @allure.title("TC-B01: 名称为空")
    def test_name_empty(self):
        add_position(
            positionName="",
            positionCode=self._code("TC_B01"),
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称不能为空"]],
        )

    @allure.title("TC-B02: 名称仅空格")
    def test_name_only_spaces(self):
        add_position(
            positionName="   ",
            positionCode=self._code("TC_B02"),
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称不能为空"]],
        )

    @allure.title("TC-B03: 名称1字符")
    def test_name_one_char(self):
        code = self._code("TC_B03")
        ts = str(int(time.time()))[-1]
        one_char_names = ["岗", "测", "A", "Z", "1", "9"]
        name = one_char_names[random.randint(0, len(one_char_names) - 1)]
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "in", [200, 500]]],
        )
        reg = register({"position_id": None})
        try:
            lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
            pid = _pid(reg)
            if pid:
                rmv_position(positionId=pid)
        except Exception:
            pass

    @allure.title("TC-B04: 名称50字符边界")
    def test_name_50_chars(self):
        code = self._code("TC_B04")
        ts = str(int(time.time()))[-6:]
        name_50 = f"TC_B04_{ts}_" + "测" * (50 - len(f"TC_B04_{ts}_"))
        add_position(
            positionName=name_50,
            positionCode=code,
            postSort=1,
            check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B05: 名称51字符超长")
    def test_name_51_chars(self):
        name_51 = "测" * 51
        add_position(
            positionName=name_51,
            positionCode=self._code("TC_B05"),
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "50"]],
        )

    @allure.title("TC-B06: 名称中文")
    def test_name_chinese(self):
        code = self._code("TC_B06")
        ts = int(time.time())
        name = f"TC_B06_高级工程师_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B07: 名称特殊字符")
    def test_name_special_chars(self):
        code = self._code("TC_B07")
        ts = int(time.time())
        name = f"TC_B07_!@#_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B08: 名称数字")
    def test_name_digits(self):
        code = self._code("TC_B08")
        ts = int(time.time())
        name = f"TC_B08_12345_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B09: 名称前后空格")
    def test_name_leading_trailing_spaces(self):
        code = self._code("TC_B09")
        ts = int(time.time())
        name = f"  TC_B09_{ts}  "
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B10: 名称换行符")
    def test_name_newline(self):
        code = self._code("TC_B10")
        ts = int(time.time())
        name = f"TC_B10_行1\n行2_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B11: 名称HTML标签")
    def test_name_html_tag(self):
        code = self._code("TC_B11")
        ts = int(time.time())
        name = f"TC_B11_<b>html</b>_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B12: 名称SQL注入尝试")
    def test_name_sql_injection(self):
        code = self._code("TC_B12")
        ts = int(time.time())
        name = f"TC_B12_sql'--_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B13: 名称XSS尝试")
    def test_name_xss(self):
        code = self._code("TC_B13")
        ts = int(time.time())
        name = f"TC_B13_<img>_{ts}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        reg = register({"position_id": None})
        lst_position(postCode=code, fetch=[[reg, "position_id", f"$.rows[?(@.postCode=='{code}')].postId"]])
        pid = _pid(reg)
        if pid:
            rmv_position(positionId=pid)

    @allure.title("TC-B14: 名称null/缺失")
    def test_name_null(self):
        add_position(
            positionCode=self._code("TC_B14"),
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称不能为空"]],
        )

    @allure.title("TC-B15: 名称超长500字符")
    def test_name_500_chars(self):
        name_500 = "x" * 500
        add_position(
            positionName=name_500,
            positionCode=self._code("TC_B15"),
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "50"]],
        )
