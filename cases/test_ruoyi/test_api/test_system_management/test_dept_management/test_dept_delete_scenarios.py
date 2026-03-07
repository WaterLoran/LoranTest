# coding: utf-8
"""
部门管理 - 删除场景测试 (TC-L1~L8)
验证删除约束、软删除行为、用户关联约束。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios001:
    """TC-L1: 删除叶子部门"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l1_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-L1: 删除叶子部门")
    def test_delete_leaf_dept_001(self):
        reg = self.reg
        name = f"lf_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        rmv_dept(deptId=reg.dept_id,
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        reg.dept_id = None

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios002:
    """TC-L2: 删除后验证列表不包含"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l2_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-L2: 删除后验证列表不包含")
    def test_deleted_not_in_list_002(self):
        reg = self.reg
        name = f"dl_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        rmv_dept(deptId=reg.dept_id, check=[["$.msg", "eq", "操作成功"]])
        reg.dept_id = None

        lst_dept(
            deptName=name,
            check=[[f"$.data[?(@.deptName=='{name}')]", "exist", False]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios003:
    """TC-L3: 有子部门不允许删除"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l3_{ts}_{rs}"
        self.reg = register({"parent_id": None, "child_id": None})

    @allure.title("TC-L3: 有子部门不允许删除")
    def test_cannot_delete_with_children_003(self):
        reg = self.reg
        p = f"p_{self.case_id}"
        c = f"c_{self.case_id}"

        add_dept(deptName=p, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p,
                 fetch=[[reg, "parent_id", f"$.data[?(@.deptName=='{p}')].deptId"]])

        add_dept(deptName=c, parentId=reg.parent_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c,
                 fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{c}')].deptId"]])

        rmv_dept(
            deptId=reg.parent_id,
            check=[["$.code", "!=", 200], ["$.msg", "include", "存在下级部门"]],
        )

    def teardown_method(self):
        for key in ["child_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios004:
    """TC-L4: 有孙子部门时删子节点 - 应失败"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l4_{ts}_{rs}"
        self.reg = register({"p_id": None, "c_id": None, "g_id": None})

    @allure.title("TC-L4: 有孙子部门时删子节点 - 应失败")
    def test_cannot_delete_child_with_grandchild_004(self):
        reg = self.reg
        p = f"p_{self.case_id}"
        c = f"c_{self.case_id}"
        g = f"g_{self.case_id}"

        add_dept(deptName=p, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p,
                 fetch=[[reg, "p_id", f"$.data[?(@.deptName=='{p}')].deptId"]])

        add_dept(deptName=c, parentId=reg.p_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c,
                 fetch=[[reg, "c_id", f"$.data[?(@.deptName=='{c}')].deptId"]])

        add_dept(deptName=g, parentId=reg.c_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=g,
                 fetch=[[reg, "g_id", f"$.data[?(@.deptName=='{g}')].deptId"]])

        rmv_dept(
            deptId=reg.c_id,
            check=[["$.code", "!=", 200], ["$.msg", "include", "存在下级部门"]],
        )

    def teardown_method(self):
        for key in ["g_id", "c_id", "p_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios005:
    """TC-L5: 删除后重建同名"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l5_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-L5: 删除后重建同名")
    def test_recreate_after_delete_005(self):
        reg = self.reg
        name = f"rb_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        rmv_dept(deptId=reg.dept_id, check=[["$.msg", "eq", "操作成功"]])
        reg.dept_id = None

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios006:
    """TC-L6: 重复删除同一部门"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l6_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-L6: 重复删除同一部门")
    def test_double_delete_006(self):
        reg = self.reg
        name = f"dd_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        rmv_dept(deptId=reg.dept_id, check=[["$.msg", "eq", "操作成功"]])
        saved_id = reg.dept_id
        reg.dept_id = None

        rmv_dept(deptId=saved_id, check=[["$.code", "==", 200]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios007:
    """TC-L7: 删除含用户的部门 - 应失败"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l7_{ts}_{rs}"
        self.reg = register({"dept_id": None, "user_id": None})

    @allure.title("TC-L7: 删除含用户的部门 - 应失败")
    def test_cannot_delete_dept_with_user_007(self):
        reg = self.reg
        name = f"du_{self.case_id}"
        user_name = f"u_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        add_user(
            userName=user_name,
            nickName=f"测试用户_{self.case_id}",
            password="admin123",
            deptId=reg.dept_id,
            phonenumber="",
            email="",
            sex="0",
            status="0",
            remark="",
            postIds=[],
            roleIds=[],
            check=[["$.msg", "eq", "操作成功"]],
        )
        lst_user(
            userName=user_name,
            fetch=[[reg, "user_id", f"$.rows[?(@.userName=='{user_name}')].userId"]],
        )

        rmv_dept(
            deptId=reg.dept_id,
            check=[["$.code", "!=", 200], ["$.msg", "include", "部门存在用户"]],
        )

    def teardown_method(self):
        if self.reg.user_id:
            try:
                rmv_user(userId=self.reg.user_id)
            except Exception:
                pass
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-删除场景")
class TestDeptDeleteScenarios008:
    """TC-L8: 删除后排除列表不包含"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"l8_{ts}_{rs}"
        self.reg = register({"dept_id": None, "ref_dept_id": None})

    @allure.title("TC-L8: 删除后排除列表不包含")
    def test_deleted_not_in_exclude_008(self):
        reg = self.reg
        name = f"de_{self.case_id}"
        ref_name = f"rf_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        add_dept(deptName=ref_name, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=ref_name,
                 fetch=[[reg, "ref_dept_id", f"$.data[?(@.deptName=='{ref_name}')].deptId"]])

        deleted_id = reg.dept_id
        rmv_dept(deptId=deleted_id, check=[["$.msg", "eq", "操作成功"]])
        reg.dept_id = None

        lst_dept_exclude(
            deptId=reg.ref_dept_id,
            fetch=[[reg, "exclude_data", "$.data"]],
            check=[["$.code", "==", 200]],
        )
        if reg.exclude_data:
            ids = [d.get("deptId") for d in reg.exclude_data if isinstance(d, dict)]
            assert deleted_id not in ids, "已删除部门不应出现在排除列表中"

    def teardown_method(self):
        if self.reg.ref_dept_id:
            try:
                rmv_dept(deptId=self.reg.ref_dept_id)
            except Exception:
                pass
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass
