# coding: utf-8
"""
角色管理 - 状态管理测试 (E类 8个用例)
status: 0=正常, 1=停用
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_status"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理-状态管理")
class TestRoleStatus:
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

    @allure.title("E01: 新增正常状态角色")
    def test_add_role_status_normal(self):
        rname = _uid("E01")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].status", "eq", "0"]],
        )

    @allure.title("E02: 新增停用状态角色")
    def test_add_role_status_disable(self):
        rname = _uid("E02")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            status="1",
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].status", "eq", "1"]],
        )

    @allure.title("E03: 启用→停用")
    def test_change_status_normal_to_disable(self):
        rname = _uid("E03")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="0")
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        change_role_status(roleId=self.reg.role_id, status="1", check=[["$.code", "eq", 200]])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.status", "eq", "1"]])

    @allure.title("E04: 停用→启用")
    def test_change_status_disable_to_normal(self):
        rname = _uid("E04")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="1")
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        change_role_status(roleId=self.reg.role_id, status="0", check=[["$.code", "eq", 200]])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.status", "eq", "0"]])

    @allure.title("E05: 停用admin角色-失败")
    def test_change_admin_status_fail(self):
        change_role_status(
            roleId=1,
            status="1",
            check=[["$.code", "eq", 500]],
        )

    @allure.title("E06: 按状态筛选正常")
    def test_lst_role_filter_status_normal(self):
        rname = _uid("E06")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="0")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            status="0",
            roleName=rname,
            check=[["$.code", "eq", 200], ["$.total", ">", 0]],
        )

    @allure.title("E07: 按状态筛选停用")
    def test_lst_role_filter_status_disable(self):
        rname = _uid("E07")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="1")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            status="1",
            roleName=rname,
            check=[["$.code", "eq", 200], ["$.total", ">", 0]],
        )

    @allure.title("E08: 停用角色后查列表验证")
    def test_disable_then_list_verify(self):
        rname = _uid("E08")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="0")
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        change_role_status(roleId=self.reg.role_id, status="1", check=[["$.code", "eq", 200]])
        lst_role(
            roleName=rname,
            status="1",
            check=[[f"$.rows[?(@.roleName=='{rname}')].status", "eq", "1"]],
        )
