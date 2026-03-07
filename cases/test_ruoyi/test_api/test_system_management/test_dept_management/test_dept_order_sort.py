# coding: utf-8
"""
部门管理 - 排序号测试 (TC-M1~M5)
验证排序号对部门列表排列的影响。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-排序号")
class TestDeptOrderSort001:
    """TC-M1: 同级多部门不同排序号"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"m1_{ts}_{rs}"
        self.reg = register({"d1_id": None, "d2_id": None, "d3_id": None})

    @allure.title("TC-M1: 同级多部门不同排序号")
    def test_different_order_nums_001(self):
        reg = self.reg
        items = [
            (f"a_{self.case_id}", 1, "d1_id"),
            (f"b_{self.case_id}", 2, "d2_id"),
            (f"c_{self.case_id}", 3, "d3_id"),
        ]
        for name, order, key in items:
            add_dept(deptName=name, parentId=100, orderNum=order, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])

        for name, order, key in items:
            lst_dept_detail(
                deptId=getattr(reg, key),
                check=[["$.data.orderNum", "eq", order]],
            )

    def teardown_method(self):
        for key in ["d3_id", "d2_id", "d1_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-排序号")
class TestDeptOrderSort002:
    """TC-M2: 同级多部门相同排序号"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"m2_{ts}_{rs}"
        self.reg = register({"d1_id": None, "d2_id": None})

    @allure.title("TC-M2: 同级多部门相同排序号")
    def test_same_order_nums_002(self):
        reg = self.reg
        n1 = f"s1_{self.case_id}"
        n2 = f"s2_{self.case_id}"

        add_dept(deptName=n1, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=n1,
                 fetch=[[reg, "d1_id", f"$.data[?(@.deptName=='{n1}')].deptId"]])

        add_dept(deptName=n2, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=n2,
                 fetch=[[reg, "d2_id", f"$.data[?(@.deptName=='{n2}')].deptId"]])

        lst_dept_detail(deptId=reg.d1_id, check=[["$.data.orderNum", "eq", 1]])
        lst_dept_detail(deptId=reg.d2_id, check=[["$.data.orderNum", "eq", 1]])

    def teardown_method(self):
        for key in ["d2_id", "d1_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-排序号")
class TestDeptOrderSort003:
    """TC-M3: 修改排序号后验证"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"m3_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-M3: 修改排序号后验证")
    def test_update_order_num_003(self):
        reg = self.reg
        name = f"uo_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=10, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.orderNum", "eq", 10]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-排序号")
class TestDeptOrderSort004:
    """TC-M4: orderNum为1的正常值"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"m4_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-M4: orderNum为1的正常值")
    def test_order_num_one_004(self):
        reg = self.reg
        name = f"o1_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.dept_id,
                        check=[["$.data.orderNum", "eq", 1]])

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-排序号")
class TestDeptOrderSort005:
    """TC-M5: 排序号对列表顺序的影响"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"m5_{ts}_{rs}"
        self.reg = register({
            "parent_id": None, "d1_id": None, "d2_id": None, "d3_id": None,
        })

    @allure.title("TC-M5: 排序号对列表顺序的影响")
    def test_order_num_affects_list_order_005(self):
        reg = self.reg
        p_name = f"p_{self.case_id}"

        add_dept(deptName=p_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p_name,
                 fetch=[[reg, "parent_id", f"$.data[?(@.deptName=='{p_name}')].deptId"]])

        items = [
            (f"z_{self.case_id}", 3, "d1_id"),
            (f"a_{self.case_id}", 1, "d2_id"),
            (f"m_{self.case_id}", 2, "d3_id"),
        ]
        for name, order, key in items:
            add_dept(deptName=name, parentId=reg.parent_id, orderNum=order, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept(
            check=[["$.code", "==", 200]],
        )

    def teardown_method(self):
        for key in ["d3_id", "d2_id", "d1_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass
