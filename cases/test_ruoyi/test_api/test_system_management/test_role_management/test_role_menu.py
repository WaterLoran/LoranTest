# coding: utf-8
"""
角色管理 - 角色菜单关联测试 (F类 10个用例)
menuIds 使用系统内置菜单 ID，属于系统固定配置数据。
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_menu"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理-菜单关联")
class TestRoleMenu:
    def setup_method(self):
        self.reg = register({"role_id": None})

    def teardown_method(self):
        if getattr(self.reg, "role_id", None):
            try:
                rmv_role(role_id=self.reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")

    @allure.title("F01: 新增角色关联单个菜单")
    def test_add_role_single_menu(self):
        rname = _uid("F01")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[1],
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.roleName", "eq", rname]])

    @allure.title("F02: 新增角色关联多个菜单")
    def test_add_role_multi_menu(self):
        rname = _uid("F02")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[1, 100, 1000, 1001],
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role_detail(
            roleId=self.reg.role_id,
            check=[["$.data.menuIds", "exist", True]],
        )

    @allure.title("F03: 新增角色不关联菜单")
    def test_add_role_no_menu(self):
        rname = _uid("F03")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[],
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        assert self.reg.role_id is not None

    @allure.title("F04: 修改角色-新增菜单")
    def test_mod_role_add_menu(self):
        rname = _uid("F04")
        add_role(roleName=rname, roleKey=rname, roleSort=1, menuIds=[1])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        mod_role(
            roleId=self.reg.role_id,
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[1, 100, 1000],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.menuIds", "exist", True]])

    @allure.title("F05: 修改角色-移除菜单")
    def test_mod_role_remove_menu(self):
        rname = _uid("F05")
        add_role(roleName=rname, roleKey=rname, roleSort=1, menuIds=[1, 100])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        mod_role(
            roleId=self.reg.role_id,
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[1],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.roleName", "eq", rname]])

    @allure.title("F06: 修改角色-替换全部菜单")
    def test_mod_role_replace_menus(self):
        rname = _uid("F06")
        add_role(roleName=rname, roleKey=rname, roleSort=1, menuIds=[1, 100])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        mod_role(
            roleId=self.reg.role_id,
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[1, 1000],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.menuIds", "exist", True]])

    @allure.title("F07: 修改角色-清空菜单")
    def test_mod_role_clear_menus(self):
        rname = _uid("F07")
        add_role(roleName=rname, roleKey=rname, roleSort=1, menuIds=[1, 100])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        mod_role(
            roleId=self.reg.role_id,
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuIds=[],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.roleName", "eq", rname]])

    @allure.title("F08: 菜单树关联显示开启")
    def test_add_role_menu_check_strictly_true(self):
        rname = _uid("F08")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuCheckStrictly=True,
            menuIds=[1, 100],
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.menuCheckStrictly", "eq", True]])

    @allure.title("F09: 菜单树关联显示关闭")
    def test_add_role_menu_check_strictly_false(self):
        rname = _uid("F09")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            menuCheckStrictly=False,
            menuIds=[1, 100],
            check=[["$.code", "eq", 200]],
        )
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.menuCheckStrictly", "eq", False]])

    @allure.title("F10: 查看角色部门树")
    def test_lst_role_dept_tree(self):
        rname = _uid("F10")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role_dept_tree(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.depts", "exist", True], ["$.checkedKeys", "exist", True]],
        )
