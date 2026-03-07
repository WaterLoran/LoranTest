# coding: utf-8
"""
部门管理 - 边界场景测试 (TC-O1~O10)
验证极端边界值和特殊输入。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary001:
    """TC-O1: 所有可选字段为空创建"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o1_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O1: 所有可选字段为空创建")
    def test_create_with_empty_optionals_001(self):
        reg = self.reg
        name = f"eo_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 leader="", phone="", email="",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.deptName", "eq", name],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary002:
    """TC-O2: deptName最大长度创建"""

    def setup_method(self):
        self.reg = register({"dept_id": None})

    @allure.title("TC-O2: deptName最大长度创建(30字符)")
    def test_create_max_length_name_002(self):
        reg = self.reg
        ts = str(int(time.time()))[-6:]
        name = f"o2{ts}" + "x" * (30 - len(f"o2{ts}"))

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.deptName", "eq", name]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary003:
    """TC-O3: 最小有效数据创建"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o3_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O3: 最小有效数据创建")
    def test_create_minimal_data_003(self):
        reg = self.reg
        name = f"mn_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=0, status="0",
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
@allure.story("部门管理-边界场景")
class TestDeptBoundary004:
    """TC-O4: leader含特殊字符"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o4_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O4: leader含特殊字符")
    def test_leader_special_chars_004(self):
        reg = self.reg
        name = f"ls_{self.case_id}"
        special_leader = "张三@#$%"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 leader=special_leader,
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.leader", "eq", special_leader]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary005:
    """TC-O5: phone恰好11位创建"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o5_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O5: phone恰好11位创建")
    def test_phone_exactly_11_create_005(self):
        reg = self.reg
        name = f"p11_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 phone="13800138000",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.phone", "eq", "13800138000"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary006:
    """TC-O6: email恰好50字符创建"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o6_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O6: email恰好50字符创建")
    def test_email_exactly_50_create_006(self):
        reg = self.reg
        name = f"e50_{self.case_id}"
        email_50 = "a" * 37 + "@example.com"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 email=email_50,
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.email", "eq", email_50]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary007:
    """TC-O7: 更新时清空所有可选字段"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o7_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O7: 更新时清空所有可选字段")
    def test_clear_all_optionals_on_update_007(self):
        reg = self.reg
        name = f"co_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 leader="有负责人", phone="13800138000", email="has@t.com",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="0", leader="", phone="", email="",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.leader", "eq", ""],
                ["$.data.phone", "eq", ""],
                ["$.data.email", "eq", ""],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary008:
    """TC-O8: deptName含中英文混合"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o8_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O8: deptName含中英文混合")
    def test_name_mixed_cn_en_008(self):
        reg = self.reg
        name = f"测试Dept{self.case_id}"
        if len(name) > 30:
            name = name[:30]

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", "$.data[0].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.deptName", "eq", name]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary009:
    """TC-O9: parentId=100顶级部门创建"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"o9_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-O9: parentId=100顶级部门创建")
    def test_create_top_level_dept_009(self):
        reg = self.reg
        name = f"tl_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.parentId", "eq", 100]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-边界场景")
class TestDeptBoundary010:
    """TC-O10: 查询超大deptId"""

    def setup_method(self):
        pass

    @allure.title("TC-O10: 查询超大deptId")
    def test_query_very_large_dept_id_010(self):
        lst_dept_detail(
            deptId=9999999999,
            check=[["$.code", "==", 200]],
        )

    def teardown_method(self):
        pass
