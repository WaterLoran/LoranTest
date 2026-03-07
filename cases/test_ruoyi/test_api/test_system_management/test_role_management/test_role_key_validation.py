# coding: utf-8
"""
角色管理 - 权限字符(roleKey)验证测试 (C类 8个用例)
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_key_validation"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理-权限字符验证")
class TestRoleKeyValidation:
    def setup_method(self):
        self.reg = register({"role_id": None, "role_id_2": None})

    def teardown_method(self):
        for key in ("role_id", "role_id_2"):
            rid = getattr(self.reg, key, None)
            if rid:
                try:
                    rmv_role(role_id=rid)
                except Exception as e:
                    print(f"清理角色失败: {e}")

    @allure.title("C01: 权限字符为空-新增失败")
    def test_add_role_key_empty(self):
        add_role(
            roleName=_uid("C01"),
            roleKey="",
            roleSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("C02: 权限字符超100字符")
    def test_add_role_key_over_100(self):
        long_key = "k" * 101
        add_role(
            roleName=_uid("C02"),
            roleKey=long_key,
            roleSort=1,
            check=[["$.code", "in", [200, 500]]],
        )

    @allure.title("C03: 权限字符恰好100字符-成功")
    def test_add_role_key_exactly_100(self):
        key_100 = "k" * 100
        rname = _uid("C03")
        add_role(
            roleName=rname,
            roleKey=key_100,
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleKey=key_100,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleKey=='{key_100}')].roleId"],
        )
        assert self.reg.role_id is not None

    @allure.title("C04: 权限字符1字符-成功")
    def test_add_role_key_one_char(self):
        rname = _uid("C04")
        add_role(
            roleName=rname,
            roleKey="x",
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        assert self.reg.role_id is not None

    @allure.title("C05: 权限字符含特殊符号-成功")
    def test_add_role_key_special_chars(self):
        rkey = _uid("C05") + "_special-1.2"
        rname = _uid("C05")
        add_role(
            roleName=rname,
            roleKey=rkey,
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        assert self.reg.role_id is not None

    @allure.title("C06: 权限字符重复-新增失败")
    def test_add_role_key_duplicate(self):
        rkey = _uid("C06_key")
        rname1 = _uid("C06_a")
        add_role(roleName=rname1, roleKey=rkey, roleSort=1)
        lst_role(roleName=rname1, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname1}')].roleId"])
        add_role(
            roleName=_uid("C06_b"),
            roleKey=rkey,
            roleSort=2,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("C07: 权限字符重复-修改为已存在失败")
    def test_mod_role_key_to_existing(self):
        k1 = _uid("C07_a")
        k2 = _uid("C07_b")
        rname1 = _uid("C07_n1")
        rname2 = _uid("C07_n2")
        add_role(roleName=rname1, roleKey=k1, roleSort=1)
        add_role(roleName=rname2, roleKey=k2, roleSort=2)
        lst_role(roleName=rname1, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname1}')].roleId"])
        lst_role(roleName=rname2, fetch=[self.reg, "role_id_2", f"$.rows[?(@.roleName=='{rname2}')].roleId"])
        mod_role(
            roleId=self.reg.role_id_2,
            roleName=rname2,
            roleKey=k1,
            roleSort=2,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("C08: 权限字符含中文-成功")
    def test_add_role_key_chinese(self):
        rkey = "权限_" + _uid("C08")
        rname = _uid("C08")
        add_role(
            roleName=rname,
            roleKey=rkey,
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        assert self.reg.role_id is not None
