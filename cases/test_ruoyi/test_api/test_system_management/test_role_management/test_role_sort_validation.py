# coding: utf-8
"""
角色管理 - 显示顺序(roleSort)验证测试 (D类 6个用例)
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_sort_validation"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理-显示顺序验证")
class TestRoleSortValidation:
    def setup_method(self):
        self.reg = register({"role_id": None})

    def teardown_method(self):
        if getattr(self.reg, "role_id", None):
            try:
                rmv_role(role_id=self.reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")

    @allure.title("D01: 顺序为空/null-新增失败")
    def test_add_role_sort_null(self):
        rname = _uid("D01")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=None,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("D02: 顺序为0-成功")
    def test_add_role_sort_zero(self):
        rname = _uid("D02")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=0,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].roleSort", "eq", 0]],
        )

    @allure.title("D03: 顺序为正整数-成功")
    def test_add_role_sort_positive(self):
        rname = _uid("D03")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=88,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].roleSort", "eq", 88]],
        )

    @allure.title("D04: 顺序为负数")
    def test_add_role_sort_negative(self):
        rname = _uid("D04")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=-1,
            check=[["$.code", "in", [200, 500]]],
        )

    @allure.title("D05: 顺序为极大值")
    def test_add_role_sort_large(self):
        rname = _uid("D05")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=999999,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].roleSort", "eq", 999999]],
        )

    @allure.title("D06: 顺序为小数-可能截断或失败")
    def test_add_role_sort_decimal(self):
        rname = _uid("D06")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=3.5,
            check=[["$.code", "in", [200, 500]]],
        )
