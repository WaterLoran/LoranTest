# coding: utf-8
"""
角色管理 - 用户授权管理测试 (H类 14个用例)
每个用例自建独立用户和角色，teardown 清理全部数据。
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_user_auth"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


def _create_user(reg, case_id):
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
        fetch=[reg, "user_id", f"$.rows[?(@.userName=='{uname}')].userId"],
    )
    reg.user_name = uname


def _create_role(reg, case_id):
    """创建本脚本专属角色并取得 roleId"""
    rname = _uid(case_id)
    add_role(roleName=rname, roleKey=rname, roleSort=1, check=[["$.code", "eq", 200]])
    lst_role(
        roleName=rname,
        fetch=[reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
    )
    reg.role_name = rname


@allure.feature("系统管理")
@allure.story("角色管理-用户授权")
class TestRoleUserAuth:
    def setup_method(self):
        self.reg = register({
            "role_id": None,
            "user_id": None,
            "user_name": None,
            "role_name": None,
        })

    def teardown_method(self):
        reg = self.reg
        if getattr(reg, "role_id", None):
            try:
                if getattr(reg, "user_id", None):
                    try:
                        cancel_auth_user(userId=reg.user_id, roleId=reg.role_id)
                    except Exception:
                        pass
                rmv_role(role_id=reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")
        if getattr(reg, "user_id", None):
            try:
                rmv_user(userId=reg.user_id)
            except Exception as e:
                print(f"清理用户失败: {e}")

    @allure.title("H01: 查看已分配用户-有数据")
    def test_lst_allocated_users_has_data(self):
        _create_role(self.reg, "H01")
        _create_user(self.reg, "H01")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.total", ">", 0]],
        )

    @allure.title("H02: 查看已分配用户-无数据")
    def test_lst_allocated_users_empty(self):
        _create_role(self.reg, "H02")
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.total", "eq", 0]],
        )

    @allure.title("H03: 查看未分配用户")
    def test_lst_unallocated_users(self):
        _create_role(self.reg, "H03")
        _create_user(self.reg, "H03")
        lst_role_unallocated_users(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("H04: 批量授权用户")
    def test_select_auth_user_all(self):
        _create_role(self.reg, "H04")
        _create_user(self.reg, "H04")
        select_auth_user_all(
            roleId=self.reg.role_id,
            userIds=[self.reg.user_id],
            check=[["$.code", "eq", 200]],
        )

    @allure.title("H05: 取消单个用户授权")
    def test_cancel_auth_user(self):
        _create_role(self.reg, "H05")
        _create_user(self.reg, "H05")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        cancel_auth_user(
            userId=self.reg.user_id,
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200]],
        )

    @allure.title("H06: 批量取消用户授权")
    def test_cancel_auth_user_all(self):
        _create_role(self.reg, "H06")
        _create_user(self.reg, "H06")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        cancel_auth_user_all(
            roleId=self.reg.role_id,
            userIds=[self.reg.user_id],
            check=[["$.code", "eq", 200]],
        )

    @allure.title("H07: 已分配用户分页")
    def test_allocated_users_pagination(self):
        _create_role(self.reg, "H07")
        _create_user(self.reg, "H07")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            pageNum=1,
            pageSize=5,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("H08: 未分配用户分页")
    def test_unallocated_users_pagination(self):
        _create_role(self.reg, "H08")
        lst_role_unallocated_users(
            roleId=self.reg.role_id,
            pageNum=1,
            pageSize=5,
            check=[["$.code", "eq", 200]],
        )

    @allure.title("H09: 已分配用户按名称搜索")
    def test_allocated_users_search_by_name(self):
        _create_role(self.reg, "H09")
        _create_user(self.reg, "H09")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            userName=self.reg.user_name,
            check=[["$.code", "eq", 200], ["$.total", ">", 0]],
        )

    @allure.title("H10: 未分配用户按名称搜索")
    def test_unallocated_users_search_by_name(self):
        _create_role(self.reg, "H10")
        _create_user(self.reg, "H10")
        lst_role_unallocated_users(
            roleId=self.reg.role_id,
            userName=self.reg.user_name,
            check=[["$.code", "eq", 200]],
        )

    @allure.title("H11: 授权后验证已分配列表")
    def test_after_assign_verify_allocated_list(self):
        _create_role(self.reg, "H11")
        _create_user(self.reg, "H11")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.total", ">", 0]],
        )

    @allure.title("H12: 取消后验证已分配列表")
    def test_after_cancel_verify_allocated_list(self):
        _create_role(self.reg, "H12")
        _create_user(self.reg, "H12")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        cancel_auth_user(userId=self.reg.user_id, roleId=self.reg.role_id)
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.total", "eq", 0]],
        )

    @allure.title("H13: 已分配用户按手机号搜索")
    def test_allocated_users_search_by_phone(self):
        _create_role(self.reg, "H13")
        _create_user(self.reg, "H13")
        select_auth_user_all(roleId=self.reg.role_id, userIds=[self.reg.user_id])
        lst_role_allocated_users(
            roleId=self.reg.role_id,
            phonenumber="",
            check=[["$.code", "eq", 200]],
        )

    @allure.title("H14: 未分配用户按手机号搜索")
    def test_unallocated_users_search_by_phone(self):
        _create_role(self.reg, "H14")
        _create_user(self.reg, "H14")
        lst_role_unallocated_users(
            roleId=self.reg.role_id,
            phonenumber="",
            check=[["$.code", "eq", 200]],
        )
