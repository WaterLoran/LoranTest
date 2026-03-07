# coding: utf-8
"""
部门管理 - 名称唯一性测试 (TC-F1~F5)
验证部门名称在同父节点下的唯一性约束。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-名称唯一性")
class TestDeptNameUniqueness001:
    """TC-F1: 同名不同父部门 - 应成功"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"f1_{ts}_{rs}"
        self.reg = register({
            "dept_id_a": None,
            "parent_b_id": None,
            "dept_id_a2": None,
        })

    @allure.title("TC-F1: 同名不同父部门 - 应成功")
    def test_same_name_different_parent_001(self):
        # Precondition operation:
        # [1]系统运行正常

        # Procedure:
        # [1]在parentId=100下创建部门A
        # [2]创建父部门B(parentId=100)
        # [3]在父部门B下创建同名部门A

        # Expected results:
        # [1]成功
        # [2]成功
        # [3]成功, 同名部门可存在于不同父节点下

        reg = self.reg
        dept_name = f"dup_{self.case_id}"
        parent_b_name = f"pb_{self.case_id}"

        # [1]在parentId=100下创建部门A
        add_dept(
            deptName=dept_name, parentId=100, orderNum=1, status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=dept_name,
            fetch=[[reg, "dept_id_a", f"$.data[?(@.deptName=='{dept_name}')].deptId"]],
        )

        # [2]创建父部门B
        add_dept(
            deptName=parent_b_name, parentId=100, orderNum=2, status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=parent_b_name,
            fetch=[[reg, "parent_b_id", f"$.data[?(@.deptName=='{parent_b_name}')].deptId"]],
        )

        # [3]在父部门B下创建同名部门A
        add_dept(
            deptName=dept_name, parentId=reg.parent_b_id, orderNum=1, status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=dept_name,
            fetch=[[reg, "dept_id_a2", f"$.data[?(@.parentId=={reg.parent_b_id})].deptId"]],
        )

    def teardown_method(self):
        if self.reg.dept_id_a2:
            try:
                rmv_dept(deptId=self.reg.dept_id_a2)
            except Exception:
                pass
        if self.reg.parent_b_id:
            try:
                rmv_dept(deptId=self.reg.parent_b_id)
            except Exception:
                pass
        if self.reg.dept_id_a:
            try:
                rmv_dept(deptId=self.reg.dept_id_a)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-名称唯一性")
class TestDeptNameUniqueness002:
    """TC-F2: 修改名称为同父已有名称 - 应失败"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"f2_{ts}_{rs}"
        self.reg = register({"dept_id_a": None, "dept_id_b": None})

    @allure.title("TC-F2: 修改名称为同父已有名称 - 应失败")
    def test_rename_to_existing_name_002(self):
        # Procedure:
        # [1]创建部门A
        # [2]创建部门B
        # [3]修改B的名称为A的名称

        # Expected results:
        # [3]code!=200, msg包含"部门名称已存在"

        reg = self.reg
        name_a = f"na_{self.case_id}"
        name_b = f"nb_{self.case_id}"

        add_dept(deptName=name_a, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name_a,
                 fetch=[[reg, "dept_id_a", f"$.data[?(@.deptName=='{name_a}')].deptId"]])

        add_dept(deptName=name_b, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name_b,
                 fetch=[[reg, "dept_id_b", f"$.data[?(@.deptName=='{name_b}')].deptId"]])

        mod_dept(
            deptId=reg.dept_id_b, deptName=name_a, parentId=100, orderNum=2, status="0",
            check=[["$.code", "!=", 200], ["$.msg", "include", "部门名称已存在"]],
        )

    def teardown_method(self):
        for did in [self.reg.dept_id_b, self.reg.dept_id_a]:
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-名称唯一性")
class TestDeptNameUniqueness003:
    """TC-F3: 删除后重新创建同名 - 应成功"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"f3_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-F3: 删除后重新创建同名 - 应成功")
    def test_recreate_after_delete_003(self):
        reg = self.reg
        dept_name = f"rc_{self.case_id}"

        add_dept(deptName=dept_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=dept_name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{dept_name}')].deptId"]])

        rmv_dept(deptId=reg.dept_id, check=[["$.msg", "eq", "操作成功"]])
        reg.dept_id = None

        add_dept(deptName=dept_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=dept_name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{dept_name}')].deptId"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-名称唯一性")
class TestDeptNameUniqueness004:
    """TC-F4: 不同状态的同父同名 - 应失败"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"f4_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-F4: 不同状态的同父同名 - 应失败")
    def test_same_name_different_status_004(self):
        reg = self.reg
        dept_name = f"ds_{self.case_id}"

        add_dept(deptName=dept_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=dept_name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{dept_name}')].deptId"]])

        add_dept(
            deptName=dept_name, parentId=100, orderNum=2, status="1",
            check=[["$.code", "!=", 200], ["$.msg", "include", "部门名称已存在"]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-名称唯一性")
class TestDeptNameUniqueness005:
    """TC-F5: 修改名称为自身原名 - 应成功"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"f5_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-F5: 修改名称为自身原名 - 应成功")
    def test_rename_to_same_name_005(self):
        reg = self.reg
        dept_name = f"sn_{self.case_id}"

        add_dept(deptName=dept_name, parentId=100, orderNum=1, status="0",
                 leader="原负责人",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=dept_name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{dept_name}')].deptId"]])

        mod_dept(
            deptId=reg.dept_id, deptName=dept_name, parentId=100, orderNum=1,
            status="0", leader="新负责人",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept_detail(
            deptId=reg.dept_id,
            check=[["$.data.deptName", "eq", dept_name], ["$.data.leader", "eq", "新负责人"]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass
