# coding: utf-8
"""
角色管理 - 角色名称验证测试 (B类 10个用例)
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_name_validation"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理-名称验证")
class TestRoleNameValidation:
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

    @allure.title("B01: 名称为空-新增失败")
    def test_add_role_name_empty(self):
        add_role(
            roleName="",
            roleKey=_uid("B01"),
            roleSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("B02: 名称超30字符-新增失败或截断")
    def test_add_role_name_over_30(self):
        long_name = "a" * 31
        add_role(
            roleName=long_name,
            roleKey=_uid("B02"),
            roleSort=1,
            check=[["$.code", "in", [200, 500]]],
        )

    @allure.title("B03: 名称恰好30字符-成功")
    def test_add_role_name_exactly_30(self):
        name_30 = ("B03_" + "名" * 15 + "a" * 15)[:30]
        rkey = _uid("B03")
        add_role(
            roleName=name_30,
            roleKey=rkey,
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=name_30,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{name_30}')].roleId"],
        )
        assert self.reg.role_id is not None

    @allure.title("B04: 名称1字符-成功")
    def test_add_role_name_one_char(self):
        rkey = _uid("B04")
        add_role(
            roleName="A",
            roleKey=rkey,
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleKey=rkey, fetch=[self.reg, "role_id", "$.rows[0].roleId"])
        assert self.reg.role_id is not None

    @allure.title("B05: 名称含特殊字符-成功")
    def test_add_role_name_special_chars(self):
        rname = _uid("B05") + "-special_1"
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        assert self.reg.role_id is not None

    @allure.title("B06: 名称含空格-成功")
    def test_add_role_name_with_space(self):
        rname = _uid("B06") + " space"
        rkey = _uid("B06_key")
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

    @allure.title("B07: 名称重复-新增失败")
    def test_add_role_name_duplicate(self):
        rname = _uid("B07")
        add_role(roleName=rname, roleKey=_uid("B07_k1"), roleSort=1)
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        add_role(
            roleName=rname,
            roleKey=_uid("B07_k2"),
            roleSort=2,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("B08: 名称重复-修改为已存在失败")
    def test_mod_role_name_to_existing(self):
        r1 = _uid("B08_a")
        r2 = _uid("B08_b")
        add_role(roleName=r1, roleKey=r1, roleSort=1)
        add_role(roleName=r2, roleKey=r2, roleSort=2)
        lst_role(roleName=r1, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{r1}')].roleId"])
        lst_role(roleName=r2, fetch=[self.reg, "role_id_2", f"$.rows[?(@.roleName=='{r2}')].roleId"])
        mod_role(
            roleId=self.reg.role_id_2,
            roleName=r1,
            roleKey=r2,
            roleSort=2,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("B09: 名称不改-修改其他字段成功")
    def test_mod_role_keep_name_change_others(self):
        rname = _uid("B09")
        add_role(roleName=rname, roleKey=rname, roleSort=1, remark="原备注")
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        mod_role(
            roleId=self.reg.role_id,
            roleName=rname,
            roleKey=rname,
            roleSort=5,
            remark="新备注",
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(
            roleId=self.reg.role_id,
            check=[
                ["$.data.roleName", "eq", rname],
                ["$.data.roleSort", "eq", 5],
                ["$.data.remark", "eq", "新备注"],
            ],
        )

    @allure.title("B10: 名称含中文-成功")
    def test_add_role_name_chinese(self):
        rname = "角色_" + _uid("B10")
        rkey = _uid("B10_key")
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
