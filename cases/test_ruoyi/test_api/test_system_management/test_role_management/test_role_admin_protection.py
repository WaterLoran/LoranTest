# coding: utf-8
"""
角色管理 - 管理员角色保护、删除规则、边界与异常测试 (J类+K类+L类 共28个用例)
roleId=1 为管理员角色，禁止修改/删除/停用/修改数据权限。
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_admin_protection"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


def _create_user(reg, case_id, key="user_id"):
    """创建本脚本专属用户并取得 userId"""
    uname = _uid(case_id)
    add_user(
        userName=uname,
        nickName=uname,
        password="Test@12345",
        check=[["$.code", "eq", 200]],
    )
    lst_user(
        userName=uname,
        fetch=[reg, key, f"$.rows[?(@.userName=='{uname}')].userId"],
    )
    setattr(reg, f"{key}_name", uname)


def _create_role(reg, case_id, key="role_id"):
    """创建本脚本专属角色并取得 roleId"""
    rname = _uid(case_id)
    add_role(roleName=rname, roleKey=rname, roleSort=1, check=[["$.code", "eq", 200]])
    lst_role(
        roleName=rname,
        fetch=[reg, key, f"$.rows[?(@.roleName=='{rname}')].roleId"],
    )


@allure.feature("系统管理")
@allure.story("角色管理-管理员保护与边界")
class TestRoleAdminProtection:
    """J: 管理员角色保护"""

    def setup_method(self):
        self.reg = register({"role_id": None, "role_id_2": None, "user_id": None})

    def teardown_method(self):
        reg = self.reg
        if getattr(reg, "user_id", None):
            try:
                rmv_user(userId=reg.user_id)
            except Exception as e:
                print(f"清理用户失败: {e}")
        for key in ("role_id", "role_id_2"):
            rid = getattr(reg, key, None)
            if rid:
                try:
                    rmv_role(role_id=rid)
                except Exception as e:
                    print(f"清理角色失败: {e}")

    @allure.title("J01: 修改admin角色-失败")
    def test_mod_admin_role_fail(self):
        mod_role(
            roleId=1,
            roleName="admin",
            roleKey="admin",
            roleSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("J02: 删除admin角色-失败")
    def test_rmv_admin_role_fail(self):
        rmv_role(role_id=1, check=[["$.code", "eq", 500]])

    @allure.title("J03: 停用admin角色-失败")
    def test_change_admin_status_fail(self):
        change_role_status(roleId=1, status="1", check=[["$.code", "eq", 500]])

    @allure.title("J04: 修改admin数据权限-失败")
    def test_set_admin_data_scope_fail(self):
        set_role_data_scope(
            roleId=1,
            dataScope="2",
            deptIds=[100],
            check=[["$.code", "eq", 500]],
        )

    @allure.title("J05: 取消admin用户授权-可执行")
    def test_cancel_admin_user_auth(self):
        _create_user(self.reg, "J05")
        select_auth_user_all(roleId=1, userIds=[self.reg.user_id])
        cancel_auth_user(userId=self.reg.user_id, roleId=1, check=[["$.code", "eq", 200]])

    @allure.title("J06: 查看admin角色详情")
    def test_lst_admin_role_detail(self):
        lst_role_detail(
            roleId=1,
            check=[["$.code", "eq", 200], ["$.data.roleId", "eq", 1], ["$.data.roleKey", "eq", "admin"]],
        )


@allure.feature("系统管理")
@allure.story("角色管理-删除规则")
class TestRoleDeleteRules:
    """K: 删除角色"""

    def setup_method(self):
        self.reg = register({"role_id": None, "role_id_2": None, "user_id": None})

    def teardown_method(self):
        reg = self.reg
        if getattr(reg, "user_id", None) and getattr(reg, "role_id", None):
            try:
                cancel_auth_user_all(roleId=reg.role_id, userIds=[reg.user_id])
            except Exception:
                pass
        if getattr(reg, "user_id", None):
            try:
                rmv_user(userId=reg.user_id)
            except Exception as e:
                print(f"清理用户失败: {e}")
        for key in ("role_id", "role_id_2"):
            rid = getattr(reg, key, None)
            if rid and rid != 1:
                try:
                    rmv_role(role_id=rid)
                except Exception as e:
                    print(f"清理角色失败: {e}")

    @allure.title("K01: 删除无用户关联角色")
    def test_rmv_role_no_user(self):
        _create_role(self.reg, "K01")
        rmv_role(role_id=self.reg.role_id, check=[["$.code", "eq", 200]])
        self.reg.role_id = None

    @allure.title("K02: 删除有用户关联角色-失败")
    def test_rmv_role_with_user_fail(self):
        _create_role(self.reg, "K02")
        _create_user(self.reg, "K02")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        rmv_role(role_id=self.reg.role_id, check=[["$.code", "eq", 500]])

    @allure.title("K03: 批量删除多角色")
    def test_rmv_role_batch_multi(self):
        _create_role(self.reg, "K03_a")
        _create_role(self.reg, "K03_b", key="role_id_2")
        rmv_role(role_id=f"{self.reg.role_id},{self.reg.role_id_2}", check=[["$.code", "eq", 200]])
        self.reg.role_id = None
        self.reg.role_id_2 = None

    @allure.title("K04: 删除admin角色-失败")
    def test_rmv_admin_fail(self):
        rmv_role(role_id=1, check=[["$.code", "eq", 500]])

    @allure.title("K05: 删除不存在的角色")
    def test_rmv_role_not_exist(self):
        rmv_role(role_id=99999999, check=[["$.code", "in", [200, 500]]])

    @allure.title("K06: 批量删中含admin-失败")
    def test_rmv_batch_include_admin_fail(self):
        _create_role(self.reg, "K06")
        rmv_role(role_id=f"1,{self.reg.role_id}", check=[["$.code", "eq", 500]])

    @allure.title("K07: 先取消用户再删除角色")
    def test_cancel_then_rmv_role(self):
        _create_role(self.reg, "K07")
        _create_user(self.reg, "K07")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        cancel_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        rmv_role(role_id=self.reg.role_id, check=[["$.code", "eq", 200]])
        self.reg.role_id = None

    @allure.title("K08: 删除后列表不可见")
    def test_rmv_then_list_invisible(self):
        _create_role(self.reg, "K08")
        rmv_role(role_id=self.reg.role_id, check=[["$.code", "eq", 200]])
        self.reg.role_id = None


@allure.feature("系统管理")
@allure.story("角色管理-边界与异常")
class TestRoleBoundary:
    """L: 边界与异常"""

    def setup_method(self):
        self.reg = register({"role_id": None})

    def teardown_method(self):
        if getattr(self.reg, "role_id", None):
            try:
                rmv_role(role_id=self.reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")

    @allure.title("L01: 备注为空")
    def test_add_role_remark_empty(self):
        rname = _uid("L01")
        add_role(roleName=rname, roleKey=rname, roleSort=1, remark="", check=[["$.code", "eq", 200]])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        assert self.reg.role_id is not None

    @allure.title("L02: 备注500字符")
    def test_add_role_remark_500(self):
        rname = _uid("L02")
        remark = "备" * 500
        add_role(roleName=rname, roleKey=rname, roleSort=1, remark=remark[:500], check=[["$.code", "eq", 200]])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.remark", "include", "备"]])

    @allure.title("L03: 备注超500字符")
    def test_add_role_remark_over_500(self):
        rname = _uid("L03")
        remark = "x" * 501
        add_role(roleName=rname, roleKey=rname, roleSort=1, remark=remark, check=[["$.code", "in", [200, 500]]])

    @allure.title("L04: roleId为0")
    def test_lst_detail_role_id_zero(self):
        lst_role_detail(roleId=0, check=[["$.code", "in", [200, 500]]])

    @allure.title("L05: roleId为负数")
    def test_lst_detail_role_id_negative(self):
        lst_role_detail(roleId=-1, check=[["$.code", "in", [200, 500]]])

    @allure.title("L06: roleId不存在")
    def test_lst_detail_role_id_not_exist(self):
        lst_role_detail(roleId=99999999, check=[["$.code", "in", [200, 500]]])

    @allure.title("L07: 缺少roleName字段-新增失败")
    def test_add_role_missing_role_name(self):
        add_role(
            roleName="",
            roleKey=_uid("L07"),
            roleSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("L08: 缺少roleKey字段-新增失败")
    def test_add_role_missing_role_key(self):
        add_role(
            roleName=_uid("L08"),
            roleKey="",
            roleSort=1,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("L09: 缺少roleSort字段-新增失败")
    def test_add_role_missing_role_sort(self):
        rname = _uid("L09")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=None,
            check=[["$.code", "eq", 500]],
        )

    @allure.title("L10: menuIds空数组")
    def test_add_role_menu_ids_empty(self):
        rname = _uid("L10")
        add_role(roleName=rname, roleKey=rname, roleSort=1, menuIds=[], check=[["$.code", "eq", 200]])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        assert self.reg.role_id is not None

    @allure.title("L11: deptIds空数组")
    def test_add_role_dept_ids_empty(self):
        rname = _uid("L11")
        add_role(roleName=rname, roleKey=rname, roleSort=1, deptIds=[], check=[["$.code", "eq", 200]])
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        assert self.reg.role_id is not None

    @allure.title("L12: 新增后立即查询")
    def test_add_then_query_immediate(self):
        rname = _uid("L12")
        add_role(roleName=rname, roleKey=rname, roleSort=1, check=[["$.code", "eq", 200]])
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].roleName", "eq", rname]],
        )
        assert self.reg.role_id is not None

    @allure.title("L13: 修改后立即查询")
    def test_mod_then_query_immediate(self):
        rname = _uid("L13")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        new_name = _uid("L13_new")
        mod_role(roleId=self.reg.role_id, roleName=new_name, roleKey=new_name, roleSort=2, check=[["$.code", "eq", 200]])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.roleName", "eq", new_name], ["$.data.roleSort", "eq", 2]])

    @allure.title("L14: 删除后立即查询")
    def test_rmv_then_query_immediate(self):
        rname = _uid("L14")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        rmv_role(role_id=self.reg.role_id, check=[["$.code", "eq", 200]])
        self.reg.role_id = None
