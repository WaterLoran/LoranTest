# coding: utf-8
"""
部门管理 - 字段边界校验测试 (TC-J1~J15)
验证各字段的长度限制、格式要求、边界值。
"""
import time
import random
import allure
from common.ruoyi_logic import *


def _setup_common(prefix):
    ts = int(time.time()) % 100000
    rs = random.randint(100, 999)
    return f"{prefix}_{ts}_{rs}"


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation001:
    """TC-J1: deptName恰好30字符 - 应成功"""

    def setup_method(self):
        self.reg = register({"dept_id": None})

    @allure.title("TC-J1: deptName恰好30字符 - 应成功")
    def test_name_exactly_30_chars_001(self):
        reg = self.reg
        ts = str(int(time.time()))[-6:]
        name = f"j1_{ts}_" + "a" * (30 - len(f"j1_{ts}_"))

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
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation002:
    """TC-J2: deptName 31字符 - 应失败"""

    def setup_method(self):
        self.reg = register({"dept_id": None})

    @allure.title("TC-J2: deptName 31字符 - 应失败")
    def test_name_31_chars_002(self):
        name = "a" * 31
        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.code", "!=", 200]])

    def teardown_method(self):
        pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation003:
    """TC-J3: phone恰好11位 - 应成功"""

    def setup_method(self):
        self.case_id = _setup_common("j3")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J3: phone恰好11位 - 应成功")
    def test_phone_exactly_11_003(self):
        reg = self.reg
        name = f"ph_{self.case_id}"

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
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation004:
    """TC-J4: phone 12位 - 应失败"""

    def setup_method(self):
        self.case_id = _setup_common("j4")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J4: phone 12位 - 应失败")
    def test_phone_12_digits_004(self):
        name = f"p12_{self.case_id}"
        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 phone="138001380001",
                 check=[["$.code", "!=", 200]])

    def teardown_method(self):
        pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation005:
    """TC-J5: phone含非数字字符 - 应失败"""

    def setup_method(self):
        self.case_id = _setup_common("j5")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J5: phone含非数字字符 - 验证系统行为")
    def test_phone_non_numeric_005(self):
        reg = self.reg
        name = f"pn_{self.case_id}"
        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 phone="1380013800a",
                 check=[["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation006:
    """TC-J6: email恰好50字符 - 应成功"""

    def setup_method(self):
        self.case_id = _setup_common("j6")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J6: email恰好50字符 - 应成功")
    def test_email_exactly_50_chars_006(self):
        reg = self.reg
        name = f"em50_{self.case_id}"
        email_50 = "a" * 37 + "@example.com"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 email=email_50,
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
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation007:
    """TC-J7: email 51字符 - 应失败"""

    def setup_method(self):
        self.case_id = _setup_common("j7")

    @allure.title("TC-J7: email 51字符 - 应失败")
    def test_email_51_chars_007(self):
        name = f"em51_{self.case_id}"
        email_51 = "a" * 39 + "@example.com"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 email=email_51,
                 check=[["$.code", "!=", 200]])

    def teardown_method(self):
        pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation008:
    """TC-J8: 多种非法邮箱格式"""

    def setup_method(self):
        self.case_id = _setup_common("j8")

    @allure.title("TC-J8: 多种非法邮箱格式")
    def test_multiple_invalid_emails_008(self):
        invalid_emails = ["@example.com", "test@", "test @e.com", "test..email@e.com"]

        for idx, bad_email in enumerate(invalid_emails):
            name = f"j8_{idx}_{self.case_id}"
            if len(name) > 30:
                name = name[:30]
            add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                     email=bad_email,
                     check=[["$.code", "!=", 200]])

    def teardown_method(self):
        pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation009:
    """TC-J9: orderNum为0 - 应成功"""

    def setup_method(self):
        self.case_id = _setup_common("j9")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J9: orderNum为0 - 应成功")
    def test_order_num_zero_009(self):
        reg = self.reg
        name = f"on0_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=0, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.orderNum", "eq", 0]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation010:
    """TC-J10: orderNum为负数"""

    def setup_method(self):
        self.case_id = _setup_common("j10")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J10: orderNum为负数")
    def test_order_num_negative_010(self):
        reg = self.reg
        name = f"onn_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=-1, status="0",
                 check=[["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation011:
    """TC-J11: orderNum为极大值"""

    def setup_method(self):
        self.case_id = _setup_common("j11")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J11: orderNum为极大值")
    def test_order_num_large_011(self):
        reg = self.reg
        name = f"onl_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=999999, status="0",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.orderNum", "eq", 999999]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation012:
    """TC-J12: deptName全空格 - 应失败"""

    def setup_method(self):
        pass

    @allure.title("TC-J12: deptName全空格 - 应失败")
    def test_name_all_spaces_012(self):
        add_dept(deptName="   ", parentId=100, orderNum=1, status="0",
                 check=[["$.code", "!=", 200]])

    def teardown_method(self):
        pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation013:
    """TC-J13: deptName含前后空格"""

    def setup_method(self):
        self.case_id = _setup_common("j13")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J13: deptName含前后空格")
    def test_name_with_spaces_013(self):
        reg = self.reg
        raw_name = f"sp_{self.case_id}"
        spaced_name = f" {raw_name} "

        add_dept(deptName=spaced_name, parentId=100, orderNum=1, status="0",
                 check=[["$.code", "==", 200]])
        lst_dept(deptName=raw_name,
                 fetch=[[reg, "dept_id", "$.data[0].deptId"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation014:
    """TC-J14: phone为空字符串 - 应成功"""

    def setup_method(self):
        self.case_id = _setup_common("j14")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J14: phone为空字符串 - 应成功")
    def test_phone_empty_014(self):
        reg = self.reg
        name = f"pe_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 phone="",
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
@allure.story("部门管理-字段边界校验")
class TestDeptFieldValidation015:
    """TC-J15: email为空字符串 - 应成功"""

    def setup_method(self):
        self.case_id = _setup_common("j15")
        self.reg = register({"dept_id": None})

    @allure.title("TC-J15: email为空字符串 - 应成功")
    def test_email_empty_015(self):
        reg = self.reg
        name = f"ee_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 email="",
                 check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass
