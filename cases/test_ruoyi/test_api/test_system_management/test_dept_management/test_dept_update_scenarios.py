# coding: utf-8
"""
部门管理 - 更新场景测试 (TC-I1~I12)
验证各字段独立/组合更新行为。
"""
import time
import random
import allure
from common.ruoyi_logic import *


def _make_dept(reg, case_id, leader="", phone="", email=""):
    """创建测试部门并获取ID的辅助方法"""
    name = f"ui_{case_id}"
    add_dept(deptName=name, parentId=100, orderNum=1, status="0",
             leader=leader, phone=phone, email=email,
             check=[["$.msg", "eq", "操作成功"]])
    lst_dept(deptName=name,
             fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
    return name


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios001:
    """TC-I1: 仅更新部门名称"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i1_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I1: 仅更新部门名称")
    def test_update_name_only_001(self):
        reg = self.reg
        old_name = _make_dept(reg, self.case_id, leader="保持不变")
        new_name = f"un_{self.case_id}"

        mod_dept(deptId=reg.dept_id, deptName=new_name, parentId=100,
                 orderNum=1, status="0", leader="保持不变",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.deptName", "eq", new_name],
                ["$.data.leader", "eq", "保持不变"],
                ["$.data.orderNum", "eq", 1],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios002:
    """TC-I2: 仅更新负责人"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i2_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I2: 仅更新负责人")
    def test_update_leader_only_002(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id, leader="旧负责人")

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="0", leader="新负责人",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.leader", "eq", "新负责人"],
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
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios003:
    """TC-I3: 仅更新电话"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i3_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I3: 仅更新电话")
    def test_update_phone_only_003(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id, phone="13800138000")

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="0", phone="13900139000",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[["$.data.phone", "eq", "13900139000"]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios004:
    """TC-I4: 仅更新邮箱"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i4_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I4: 仅更新邮箱")
    def test_update_email_only_004(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id, email="old@test.com")

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="0", email="new@test.com",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[["$.data.email", "eq", "new@test.com"]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios005:
    """TC-I5: 仅更新排序号"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i5_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I5: 仅更新排序号")
    def test_update_order_num_only_005(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id)

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=99, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[["$.data.orderNum", "eq", 99]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios006:
    """TC-I6: 仅更新状态"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i6_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I6: 仅更新状态")
    def test_update_status_only_006(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id)

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[["$.data.status", "eq", "1"]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios007:
    """TC-I7: 同时更新所有字段"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i7_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I7: 同时更新所有字段")
    def test_update_all_fields_007(self):
        reg = self.reg
        _make_dept(reg, self.case_id, leader="旧", phone="13800138000", email="old@t.com")
        new_name = f"nw_{self.case_id}"

        mod_dept(
            deptId=reg.dept_id, deptName=new_name, parentId=100,
            orderNum=50, status="0",
            leader="新负责人", phone="13900139000", email="new@t.com",
            check=[["$.msg", "eq", "操作成功"]],
        )

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.deptName", "eq", new_name],
                ["$.data.orderNum", "eq", 50],
                ["$.data.leader", "eq", "新负责人"],
                ["$.data.phone", "eq", "13900139000"],
                ["$.data.email", "eq", "new@t.com"],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios008:
    """TC-I8: 更新为相同值(无实际变化)"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i8_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I8: 更新为相同值(无实际变化)")
    def test_update_same_values_008(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id, leader="不变负责人", phone="13800138000")

        mod_dept(
            deptId=reg.dept_id, deptName=name, parentId=100,
            orderNum=1, status="0", leader="不变负责人", phone="13800138000",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.deptName", "eq", name],
                ["$.data.leader", "eq", "不变负责人"],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios009:
    """TC-I9: 更新名称为空 - 应失败"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i9_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I9: 更新名称为空 - 应失败")
    def test_update_name_to_empty_009(self):
        reg = self.reg
        _make_dept(reg, self.case_id)

        mod_dept(
            deptId=reg.dept_id, deptName="", parentId=100,
            orderNum=1, status="0",
            check=[["$.code", "!=", 200]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios010:
    """TC-I10: 更新时orderNum使用默认值0"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i10_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I10: 更新时orderNum使用默认值0")
    def test_update_order_num_default_010(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id)

        mod_dept(
            deptId=reg.dept_id, deptName=name, parentId=100,
            orderNum=0, status="0",
            check=[["$.code", "==", 200]],
        )

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[["$.data.orderNum", "eq", 0]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios011:
    """TC-I11: 清空可选字段(leader/phone/email)"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i11_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I11: 清空可选字段(leader/phone/email)")
    def test_clear_optional_fields_011(self):
        reg = self.reg
        name = _make_dept(reg, self.case_id, leader="有负责人", phone="13800138000",
                          email="has@test.com")

        mod_dept(
            deptId=reg.dept_id, deptName=name, parentId=100,
            orderNum=1, status="0", leader="", phone="", email="",
            check=[["$.msg", "eq", "操作成功"]],
        )

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
@allure.story("部门管理-更新场景")
class TestDeptUpdateScenarios012:
    """TC-I12: 更新后查询详情验证所有字段"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"i12_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-I12: 更新后查询详情验证所有字段")
    def test_full_field_verify_after_update_012(self):
        reg = self.reg
        _make_dept(reg, self.case_id)
        new_name = f"vf_{self.case_id}"

        mod_dept(
            deptId=reg.dept_id, deptName=new_name, parentId=100,
            orderNum=77, status="0",
            leader="验证负责人", phone="13700137000", email="vf@test.com",
            check=[["$.msg", "eq", "操作成功"]],
        )

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.code", "==", 200],
                ["$.data.deptName", "eq", new_name],
                ["$.data.parentId", "eq", 100],
                ["$.data.orderNum", "eq", 77],
                ["$.data.status", "eq", "0"],
                ["$.data.leader", "eq", "验证负责人"],
                ["$.data.phone", "eq", "13700137000"],
                ["$.data.email", "eq", "vf@test.com"],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass
