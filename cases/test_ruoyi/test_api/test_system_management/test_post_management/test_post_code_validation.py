#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 岗位编码验证测试 (TC-C01~TC-C15)
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
class TestPostCodeValidation(object):
    """岗位编码验证"""

    def setup_method(self):
        self.reg = register({"position_id": None, "position_id2": None})

    def _name(self, case_id):
        return f"{case_id}_{int(time.time())}_{random.randint(1000, 9999)}"

    def teardown_method(self):
        for key in ("position_id", "position_id2"):
            pid = getattr(self.reg, key, None)
            if isinstance(pid, list) and pid:
                pid = pid[0]
            if pid:
                try:
                    rmv_position(positionId=pid)
                except Exception:
                    pass

    @allure.title("TC-C01: 编码为空")
    def test_code_empty(self):
        add_position(
            positionName=self._name("TC_C01"),
            positionCode="",
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码不能为空"]],
        )

    @allure.title("TC-C02: 编码仅空格")
    def test_code_only_spaces(self):
        add_position(
            positionName=self._name("TC_C02"),
            positionCode="   ",
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码不能为空"]],
        )

    @allure.title("TC-C03: 编码1字符-应允许创建")
    def test_code_one_char(self):
        name = self._name("TC_C03")
        code = random.choice(["x", "y", "z", "a", "b"])
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C04: 编码64字符边界")
    def test_code_64_chars(self):
        name = self._name("TC_C04")
        ts = str(int(time.time()))
        code_64 = f"TC_C04_{ts}_" + "a" * (64 - len(f"TC_C04_{ts}_"))
        add_position(
            positionName=name,
            positionCode=code_64,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C05: 编码65字符超长")
    def test_code_65_chars(self):
        code_65 = "a" * 65
        add_position(
            positionName=self._name("TC_C05"),
            positionCode=code_65,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "64"]],
        )

    @allure.title("TC-C06: 编码纯数字")
    def test_code_digits(self):
        name = self._name("TC_C06")
        ts = int(time.time())
        code = f"{ts}{random.randint(100, 999)}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C07: 编码字母数字")
    def test_code_alpha_num(self):
        name = self._name("TC_C07")
        code = f"TC_C07_cd{int(time.time())}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C08: 编码下划线")
    def test_code_underscore(self):
        name = self._name("TC_C08")
        code = f"TC_C08_ab_{int(time.time())}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C09: 编码中文")
    def test_code_chinese(self):
        name = self._name("TC_C09")
        code = f"TC_C09_编码_{int(time.time())}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C10: 编码特殊字符")
    def test_code_special(self):
        name = self._name("TC_C10")
        code = f"TC_C10-1.2_{int(time.time())}"
        add_position(
            positionName=name,
            positionCode=code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(postName=name, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]])

    @allure.title("TC-C11: 编码前后空格-系统应自动trim后存储")
    def test_code_leading_trailing_spaces(self):
        name = self._name("TC_C11")
        ts = int(time.time())
        code_with_spaces = f"  TC_C11_{ts}  "
        code_trimmed = f"TC_C11_{ts}"
        add_position(
            positionName=name,
            positionCode=code_with_spaces,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name}')].postId"]],
        )
        lst_position_detail(
            positionId=_pid(self.reg),
            check=[["$.data.postCode", "eq", code_trimmed]],
        )

    @allure.title("TC-C12: 编码null/缺失")
    def test_code_null(self):
        add_position(
            positionName=self._name("TC_C12"),
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码不能为空"]],
        )

    @allure.title("TC-C13: 编码大小写区分-大小写不同应视为不同编码")
    def test_code_case_sensitive(self):
        ts = int(time.time())
        name1 = self._name("TC_C13_a")
        name2 = self._name("TC_C13_b")
        code_a = f"TC_C13_Abc_{ts}"
        code_b = f"TC_C13_abc_{ts}"
        add_position(positionName=name1, positionCode=code_a, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name1, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name1}')].postId"]])
        add_position(positionName=name2, positionCode=code_b, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])

    @allure.title("TC-C14: 编码与名称同值")
    def test_code_same_as_name(self):
        same = f"TC_C14_{int(time.time())}"
        add_position(positionName=same, positionCode=same, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postCode=same, fetch=[[self.reg, "position_id", f"$.rows[?(@.postCode=='{same}')].postId"]])

    @allure.title("TC-C15: 编码超长128字符")
    def test_code_128_chars(self):
        code_128 = "a" * 128
        add_position(
            positionName=self._name("TC_C15"),
            positionCode=code_128,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "64"]],
        )
