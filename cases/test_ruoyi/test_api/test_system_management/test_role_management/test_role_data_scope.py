# coding: utf-8
"""
角色管理 - 数据权限测试 (G类 10个用例)
dataScope: 1=全部 2=自定义 3=本部门 4=本部门及以下 5=仅本人
每个自定义权限用例自建专属部门，teardown 清理。
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_data_scope"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


def _create_role(reg, case_id, key="role_id"):
    rname = _uid(case_id)
    add_role(roleName=rname, roleKey=rname, roleSort=1, check=[["$.code", "eq", 200]])
    lst_role(
        roleName=rname,
        fetch=[reg, key, f"$.rows[?(@.roleName=='{rname}')].roleId"],
    )


def _create_dept(reg, case_id, key="dept_id"):
    dname = _uid(case_id)
    add_dept(parentId=100, deptName=dname, orderNum=1, check=[["$.code", "eq", 200]])
    lst_dept(
        deptName=dname,
        fetch=[reg, key, f"$..[?(@.deptName=='{dname}')].deptId"],
    )


@allure.feature("系统管理")
@allure.story("角色管理-数据权限")
class TestRoleDataScope:
    def setup_method(self):
        self.reg = register({
            "role_id": None,
            "dept_id": None,
            "dept_id_2": None,
            "dept_id_3": None,
        })

    def teardown_method(self):
        reg = self.reg
        if getattr(reg, "role_id", None):
            try:
                rmv_role(role_id=reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")
        for key in ("dept_id", "dept_id_2", "dept_id_3"):
            did = getattr(reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception as e:
                    print(f"清理部门失败: {e}")

    @allure.title("G01: 全部数据权限 scope=1")
    def test_set_data_scope_all(self):
        _create_role(self.reg, "G01")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="1",
            deptIds=[],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "1"]])

    @allure.title("G02: 自定义数据权限 scope=2")
    def test_set_data_scope_custom(self):
        _create_role(self.reg, "G02")
        _create_dept(self.reg, "G02_d1")
        _create_dept(self.reg, "G02_d2", key="dept_id_2")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="2",
            deptIds=[self.reg.dept_id, self.reg.dept_id_2],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "2"]])

    @allure.title("G03: 本部门数据权限 scope=3")
    def test_set_data_scope_dept(self):
        _create_role(self.reg, "G03")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="3",
            deptIds=[],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "3"]])

    @allure.title("G04: 本部门及以下 scope=4")
    def test_set_data_scope_dept_and_child(self):
        _create_role(self.reg, "G04")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="4",
            deptIds=[],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "4"]])

    @allure.title("G05: 仅本人数据权限 scope=5")
    def test_set_data_scope_self(self):
        _create_role(self.reg, "G05")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="5",
            deptIds=[],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "5"]])

    @allure.title("G06: 自定义权限关联多部门")
    def test_set_data_scope_custom_multi_dept(self):
        _create_role(self.reg, "G06")
        _create_dept(self.reg, "G06_d1")
        _create_dept(self.reg, "G06_d2", key="dept_id_2")
        _create_dept(self.reg, "G06_d3", key="dept_id_3")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="2",
            deptIds=[self.reg.dept_id, self.reg.dept_id_2, self.reg.dept_id_3],
            check=[["$.code", "eq", 200]],
        )
        lst_role_dept_tree(
            roleId=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.checkedKeys", "exist", True]],
        )

    @allure.title("G07: 自定义权限关联单部门")
    def test_set_data_scope_custom_single_dept(self):
        _create_role(self.reg, "G07")
        _create_dept(self.reg, "G07_d1")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="2",
            deptIds=[self.reg.dept_id],
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "2"]])

    @allure.title("G08: 修改数据权限-切换类型")
    def test_set_data_scope_switch_type(self):
        _create_role(self.reg, "G08")
        _create_dept(self.reg, "G08_d1")
        set_role_data_scope(roleId=self.reg.role_id, dataScope="1", deptIds=[], check=[["$.code", "eq", 200]])
        set_role_data_scope(roleId=self.reg.role_id, dataScope="2", deptIds=[self.reg.dept_id], check=[["$.code", "eq", 200]])
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.dataScope", "eq", "2"]])

    @allure.title("G09: 部门树关联显示开启")
    def test_set_data_scope_dept_check_strictly_true(self):
        _create_role(self.reg, "G09")
        _create_dept(self.reg, "G09_d1")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="2",
            deptIds=[self.reg.dept_id],
            deptCheckStrictly=True,
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.deptCheckStrictly", "eq", True]])

    @allure.title("G10: 部门树关联显示关闭")
    def test_set_data_scope_dept_check_strictly_false(self):
        _create_role(self.reg, "G10")
        _create_dept(self.reg, "G10_d1")
        set_role_data_scope(
            roleId=self.reg.role_id,
            dataScope="2",
            deptIds=[self.reg.dept_id],
            deptCheckStrictly=False,
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.deptCheckStrictly", "eq", False]])
