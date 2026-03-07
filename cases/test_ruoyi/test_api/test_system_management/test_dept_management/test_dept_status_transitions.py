# coding: utf-8
"""
部门管理 - 状态转换测试 (TC-H1~H8)
验证状态切换、联动、筛选等场景。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions001:
    """TC-H1: 启用已停用部门"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h1_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-H1: 启用已停用部门")
    def test_enable_disabled_dept_001(self):
        reg = self.reg
        name = f"ed_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100, orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept_detail(deptId=reg.dept_id, check=[["$.data.status", "eq", "1"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept_detail(deptId=reg.dept_id, check=[["$.data.status", "eq", "0"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions002:
    """TC-H2: 状态来回切换 0→1→0"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h2_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-H2: 状态来回切换 0→1→0")
    def test_toggle_status_002(self):
        reg = self.reg
        name = f"tg_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100, orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept_detail(deptId=reg.dept_id, check=[["$.data.status", "eq", "1"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept_detail(deptId=reg.dept_id, check=[["$.data.status", "eq", "0"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions003:
    """TC-H3: 按状态=0筛选列表"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h3_{ts}_{rs}"
        self.reg = register({"dept_a_id": None, "dept_b_id": None})

    @allure.title("TC-H3: 按状态=0筛选列表")
    def test_filter_status_normal_003(self):
        reg = self.reg
        a_name = f"sa_{self.case_id}"
        b_name = f"sb_{self.case_id}"

        add_dept(deptName=a_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a_name,
                 fetch=[[reg, "dept_a_id", f"$.data[?(@.deptName=='{a_name}')].deptId"]])

        add_dept(deptName=b_name, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=b_name,
                 fetch=[[reg, "dept_b_id", f"$.data[?(@.deptName=='{b_name}')].deptId"]])
        mod_dept(deptId=reg.dept_b_id, deptName=b_name, parentId=100, orderNum=2, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept(
            status="0",
            check=[
                [f"$.data[?(@.deptName=='{a_name}')]", "exist", True],
            ],
        )

    def teardown_method(self):
        for key in ["dept_b_id", "dept_a_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions004:
    """TC-H4: 按状态=1筛选列表"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h4_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-H4: 按状态=1筛选列表")
    def test_filter_status_disabled_004(self):
        reg = self.reg
        name = f"sd_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100, orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept(
            status="1",
            check=[
                [f"$.data[?(@.deptName=='{name}')]", "exist", True],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions005:
    """TC-H5: 启用部门时祖先自动启用"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h5_{ts}_{rs}"
        self.reg = register({"parent_id": None, "child_id": None})

    @allure.title("TC-H5: 启用部门时祖先自动启用")
    def test_enable_dept_enables_ancestors_005(self):
        reg = self.reg
        p_name = f"p_{self.case_id}"
        c_name = f"c_{self.case_id}"

        add_dept(deptName=p_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p_name,
                 fetch=[[reg, "parent_id", f"$.data[?(@.deptName=='{p_name}')].deptId"]])

        add_dept(deptName=c_name, parentId=reg.parent_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c_name,
                 fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{c_name}')].deptId"]])

        mod_dept(deptId=reg.child_id, deptName=c_name, parentId=reg.parent_id,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])
        mod_dept(deptId=reg.parent_id, deptName=p_name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        mod_dept(deptId=reg.child_id, deptName=c_name, parentId=reg.parent_id,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(deptId=reg.parent_id,
                        check=[["$.data.status", "eq", "0"]])

    def teardown_method(self):
        for key in ["child_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions006:
    """TC-H6: 停用叶子部门(无子部门)"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h6_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-H6: 停用叶子部门(无子部门)")
    def test_disable_leaf_dept_006(self):
        reg = self.reg
        name = f"lf_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions007:
    """TC-H7: 先停用所有子部门再停用父部门"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h7_{ts}_{rs}"
        self.reg = register({"parent_id": None, "child_id": None})

    @allure.title("TC-H7: 先停用所有子部门再停用父部门")
    def test_disable_children_then_parent_007(self):
        reg = self.reg
        p_name = f"p_{self.case_id}"
        c_name = f"c_{self.case_id}"

        add_dept(deptName=p_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p_name,
                 fetch=[[reg, "parent_id", f"$.data[?(@.deptName=='{p_name}')].deptId"]])

        add_dept(deptName=c_name, parentId=reg.parent_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c_name,
                 fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{c_name}')].deptId"]])

        mod_dept(deptId=reg.child_id, deptName=c_name, parentId=reg.parent_id,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        mod_dept(deptId=reg.parent_id, deptName=p_name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(deptId=reg.parent_id, check=[["$.data.status", "eq", "1"]])
        lst_dept_detail(deptId=reg.child_id, check=[["$.data.status", "eq", "1"]])

    def teardown_method(self):
        for key in ["child_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-状态转换")
class TestDeptStatusTransitions008:
    """TC-H8: 停用后查询详情验证状态"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"h8_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-H8: 停用后查询详情验证状态")
    def test_verify_status_after_disable_008(self):
        reg = self.reg
        name = f"vd_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 leader="测试人", phone="13800138000", email="h8@test.com",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="1", leader="测试人",
                 phone="13800138000", email="h8@test.com",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.status", "eq", "1"],
                ["$.data.deptName", "eq", name],
                ["$.data.leader", "eq", "测试人"],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass
