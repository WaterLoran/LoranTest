# coding: utf-8
"""
部门管理 - 集成场景测试 (TC-N1~N8)
验证多步骤复杂业务流程。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration001:
    """TC-N1: 完整树创建后从底向上删除"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n1_{ts}_{rs}"
        self.reg = register({"p_id": None, "c_id": None, "g_id": None})

    @allure.title("TC-N1: 完整树创建后从底向上删除")
    def test_create_tree_delete_bottom_up_001(self):
        reg = self.reg
        p = f"p_{self.case_id}"
        c = f"c_{self.case_id}"
        g = f"g_{self.case_id}"

        add_dept(deptName=p, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p, fetch=[[reg, "p_id", f"$.data[?(@.deptName=='{p}')].deptId"]])

        add_dept(deptName=c, parentId=reg.p_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c, fetch=[[reg, "c_id", f"$.data[?(@.deptName=='{c}')].deptId"]])

        add_dept(deptName=g, parentId=reg.c_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=g, fetch=[[reg, "g_id", f"$.data[?(@.deptName=='{g}')].deptId"]])

        rmv_dept(deptId=reg.g_id, check=[["$.msg", "eq", "操作成功"]])
        reg.g_id = None
        rmv_dept(deptId=reg.c_id, check=[["$.msg", "eq", "操作成功"]])
        reg.c_id = None
        rmv_dept(deptId=reg.p_id, check=[["$.msg", "eq", "操作成功"]])
        reg.p_id = None

    def teardown_method(self):
        for key in ["g_id", "c_id", "p_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration002:
    """TC-N2: 创建后修改父节点验证树变化"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n2_{ts}_{rs}"
        self.reg = register({"a_id": None, "b_id": None, "c_id": None})

    @allure.title("TC-N2: 创建后修改父节点验证树变化")
    def test_move_and_verify_tree_002(self):
        reg = self.reg
        a = f"a_{self.case_id}"
        b = f"b_{self.case_id}"
        c = f"c_{self.case_id}"

        add_dept(deptName=a, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a, fetch=[[reg, "a_id", f"$.data[?(@.deptName=='{a}')].deptId"]])

        add_dept(deptName=b, parentId=reg.a_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=b, fetch=[[reg, "b_id", f"$.data[?(@.deptName=='{b}')].deptId"]])

        add_dept(deptName=c, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c, fetch=[[reg, "c_id", f"$.data[?(@.deptName=='{c}')].deptId"]])

        mod_dept(deptId=reg.b_id, deptName=b, parentId=reg.c_id,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(deptId=reg.b_id,
                        check=[["$.data.parentId", "eq", reg.c_id]])

    def teardown_method(self):
        for key in ["b_id", "c_id", "a_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration003:
    """TC-N3: 批量创建5+部门"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n3_{ts}_{rs}"
        self.dept_ids = []
        self.reg = register({})

    @allure.title("TC-N3: 批量创建5+部门")
    def test_batch_create_depts_003(self):
        reg = self.reg
        for i in range(5):
            name = f"bt{i}_{self.case_id}"
            key = f"d{i}_id"
            setattr(reg, key, None)
            add_dept(deptName=name, parentId=100, orderNum=i + 1, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])
            self.dept_ids.append(key)

        for key in self.dept_ids:
            did = getattr(reg, key, None)
            assert did is not None, f"{key} 应不为空"

    def teardown_method(self):
        for key in reversed(self.dept_ids):
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration004:
    """TC-N4: 链式创建 root→d1→d2→d3→d4"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n4_{ts}_{rs}"
        self.reg = register({
            "d1_id": None, "d2_id": None, "d3_id": None, "d4_id": None,
        })

    @allure.title("TC-N4: 链式创建 root→d1→d2→d3→d4")
    def test_chain_create_004(self):
        reg = self.reg
        keys = ["d1_id", "d2_id", "d3_id", "d4_id"]
        parent = 100

        for i, key in enumerate(keys):
            name = f"ch{i}_{self.case_id}"
            add_dept(deptName=name, parentId=parent, orderNum=1, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])
            parent = getattr(reg, key)

        lst_dept_detail(deptId=reg.d4_id,
                        check=[["$.data.parentId", "eq", reg.d3_id]])

    def teardown_method(self):
        for key in ["d4_id", "d3_id", "d2_id", "d1_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration005:
    """TC-N5: 树修改后排除列表验证"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n5_{ts}_{rs}"
        self.reg = register({
            "p_id": None, "ca_id": None, "a1_id": None, "cb_id": None,
        })

    @allure.title("TC-N5: 树修改后排除列表验证")
    def test_exclude_after_tree_modify_005(self):
        reg = self.reg
        p = f"p_{self.case_id}"
        ca = f"ca_{self.case_id}"
        a1 = f"a1_{self.case_id}"
        cb = f"cb_{self.case_id}"

        add_dept(deptName=p, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p, fetch=[[reg, "p_id", f"$.data[?(@.deptName=='{p}')].deptId"]])

        add_dept(deptName=ca, parentId=reg.p_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=ca, fetch=[[reg, "ca_id", f"$.data[?(@.deptName=='{ca}')].deptId"]])

        add_dept(deptName=a1, parentId=reg.ca_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a1, fetch=[[reg, "a1_id", f"$.data[?(@.deptName=='{a1}')].deptId"]])

        add_dept(deptName=cb, parentId=reg.p_id, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=cb, fetch=[[reg, "cb_id", f"$.data[?(@.deptName=='{cb}')].deptId"]])

        lst_dept_exclude(
            deptId=reg.ca_id,
            fetch=[[reg, "exclude_data", "$.data"]],
            check=[["$.code", "==", 200]],
        )
        if reg.exclude_data:
            ids = [d.get("deptId") for d in reg.exclude_data if isinstance(d, dict)]
            assert reg.ca_id not in ids
            assert reg.a1_id not in ids

    def teardown_method(self):
        for key in ["a1_id", "cb_id", "ca_id", "p_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration006:
    """TC-N6: 子部门在父部门间移动"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n6_{ts}_{rs}"
        self.reg = register({"a_id": None, "b_id": None, "c_id": None})

    @allure.title("TC-N6: 子部门在父部门间移动")
    def test_move_child_between_parents_006(self):
        reg = self.reg
        a = f"a_{self.case_id}"
        b = f"b_{self.case_id}"
        c = f"c_{self.case_id}"

        add_dept(deptName=a, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a, fetch=[[reg, "a_id", f"$.data[?(@.deptName=='{a}')].deptId"]])

        add_dept(deptName=b, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=b, fetch=[[reg, "b_id", f"$.data[?(@.deptName=='{b}')].deptId"]])

        add_dept(deptName=c, parentId=reg.a_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c, fetch=[[reg, "c_id", f"$.data[?(@.deptName=='{c}')].deptId"]])

        lst_dept_detail(deptId=reg.c_id, check=[["$.data.parentId", "eq", reg.a_id]])

        mod_dept(deptId=reg.c_id, deptName=c, parentId=reg.b_id,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(deptId=reg.c_id, check=[["$.data.parentId", "eq", reg.b_id]])

    def teardown_method(self):
        for key in ["c_id", "b_id", "a_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration007:
    """TC-N7: 全字段完整生命周期"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n7_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-N7: 全字段完整生命周期")
    def test_full_field_lifecycle_007(self):
        reg = self.reg
        name = f"fl_{self.case_id}"

        add_dept(
            deptName=name, parentId=100, orderNum=1, status="0",
            leader="张三", phone="13800138000", email="zs@test.com",
            check=[["$.msg", "eq", "操作成功"]],
        )
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.deptName", "eq", name],
                ["$.data.orderNum", "eq", 1],
                ["$.data.leader", "eq", "张三"],
                ["$.data.phone", "eq", "13800138000"],
                ["$.data.email", "eq", "zs@test.com"],
                ["$.data.status", "eq", "0"],
            ],
        )

        new_name = f"uf_{self.case_id}"
        mod_dept(
            deptId=reg.dept_id, deptName=new_name, parentId=100,
            orderNum=5, status="0",
            leader="李四", phone="13900139000", email="ls@test.com",
            check=[["$.msg", "eq", "操作成功"]],
        )

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.deptName", "eq", new_name],
                ["$.data.orderNum", "eq", 5],
                ["$.data.leader", "eq", "李四"],
                ["$.data.phone", "eq", "13900139000"],
                ["$.data.email", "eq", "ls@test.com"],
            ],
        )

        rmv_dept(deptId=reg.dept_id, check=[["$.msg", "eq", "操作成功"]])
        reg.dept_id = None

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-集成场景")
class TestDeptIntegration008:
    """TC-N8: 多分支树结构验证"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"n8_{ts}_{rs}"
        self.reg = register({
            "root_id": None,
            "a_id": None, "b_id": None,
            "a1_id": None, "a2_id": None, "b1_id": None,
        })

    @allure.title("TC-N8: 多分支树结构验证")
    def test_multi_branch_tree_008(self):
        reg = self.reg
        root = f"rt_{self.case_id}"

        add_dept(deptName=root, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=root,
                 fetch=[[reg, "root_id", f"$.data[?(@.deptName=='{root}')].deptId"]])

        branches = [
            (f"a_{self.case_id}", reg.root_id, "a_id", 1),
            (f"b_{self.case_id}", reg.root_id, "b_id", 2),
        ]
        for name, pid, key, order in branches:
            add_dept(deptName=name, parentId=pid, orderNum=order, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])

        leaves = [
            (f"a1_{self.case_id}", reg.a_id, "a1_id", 1),
            (f"a2_{self.case_id}", reg.a_id, "a2_id", 2),
            (f"b1_{self.case_id}", reg.b_id, "b1_id", 1),
        ]
        for name, pid, key, order in leaves:
            add_dept(deptName=name, parentId=pid, orderNum=order, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept_detail(deptId=reg.a_id, check=[["$.data.parentId", "eq", reg.root_id]])
        lst_dept_detail(deptId=reg.b_id, check=[["$.data.parentId", "eq", reg.root_id]])
        lst_dept_detail(deptId=reg.a1_id, check=[["$.data.parentId", "eq", reg.a_id]])
        lst_dept_detail(deptId=reg.a2_id, check=[["$.data.parentId", "eq", reg.a_id]])
        lst_dept_detail(deptId=reg.b1_id, check=[["$.data.parentId", "eq", reg.b_id]])

    def teardown_method(self):
        for key in ["b1_id", "a2_id", "a1_id", "b_id", "a_id", "root_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass
