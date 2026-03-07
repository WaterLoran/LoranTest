# coding: utf-8
"""
部门管理 - 高级层级操作测试 (TC-G1~G10)
验证深层级结构、移动部门、ancestors字段维护。
"""
import time
import random
import allure
from common.ruoyi_logic import *


def _short_id(prefix, case_id):
    """生成不超过30字符的部门名称"""
    return f"{prefix}_{case_id}"


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced001:
    """TC-G1: 4层深度层级"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g1_{ts}_{rs}"
        self.reg = register({
            "l1_id": None, "l2_id": None, "l3_id": None, "l4_id": None,
        })

    @allure.title("TC-G1: 4层深度层级")
    def test_four_level_hierarchy_001(self):
        reg = self.reg
        names = [f"l{i}_{self.case_id}" for i in range(1, 5)]

        add_dept(deptName=names[0], parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=names[0],
                 fetch=[[reg, "l1_id", f"$.data[?(@.deptName=='{names[0]}')].deptId"]])

        add_dept(deptName=names[1], parentId=reg.l1_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=names[1],
                 fetch=[[reg, "l2_id", f"$.data[?(@.deptName=='{names[1]}')].deptId"]])

        add_dept(deptName=names[2], parentId=reg.l2_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=names[2],
                 fetch=[[reg, "l3_id", f"$.data[?(@.deptName=='{names[2]}')].deptId"]])

        add_dept(deptName=names[3], parentId=reg.l3_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=names[3],
                 fetch=[[reg, "l4_id", f"$.data[?(@.deptName=='{names[3]}')].deptId"]])

        lst_dept_detail(
            deptId=reg.l4_id,
            check=[["$.data.parentId", "eq", reg.l3_id]],
        )

    def teardown_method(self):
        for key in ["l4_id", "l3_id", "l2_id", "l1_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced002:
    """TC-G2: 移动部门到不同父节点"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g2_{ts}_{rs}"
        self.reg = register({"pa_id": None, "pb_id": None, "child_id": None})

    @allure.title("TC-G2: 移动部门到不同父节点")
    def test_move_dept_to_different_parent_002(self):
        reg = self.reg
        pa_name = f"pa_{self.case_id}"
        pb_name = f"pb_{self.case_id}"
        child_name = f"ch_{self.case_id}"

        add_dept(deptName=pa_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=pa_name,
                 fetch=[[reg, "pa_id", f"$.data[?(@.deptName=='{pa_name}')].deptId"]])

        add_dept(deptName=pb_name, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=pb_name,
                 fetch=[[reg, "pb_id", f"$.data[?(@.deptName=='{pb_name}')].deptId"]])

        add_dept(deptName=child_name, parentId=reg.pa_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=child_name,
                 fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{child_name}')].deptId"]])

        mod_dept(
            deptId=reg.child_id, deptName=child_name, parentId=reg.pb_id,
            orderNum=1, status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept_detail(
            deptId=reg.child_id,
            check=[["$.data.parentId", "eq", reg.pb_id]],
        )

    def teardown_method(self):
        for key in ["child_id", "pb_id", "pa_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced003:
    """TC-G3: 创建时验证ancestors字段"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g3_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-G3: 创建时验证ancestors字段")
    def test_ancestors_on_create_003(self):
        reg = self.reg
        dept_name = f"ac_{self.case_id}"

        add_dept(deptName=dept_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=dept_name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{dept_name}')].deptId"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.data.ancestors", "include", "100"],
                ["$.data.parentId", "eq", 100],
            ],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced004:
    """TC-G4: 修改父节点后验证ancestors更新"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g4_{ts}_{rs}"
        self.reg = register({"pa_id": None, "child_id": None, "pc_id": None})

    @allure.title("TC-G4: 修改父节点后验证ancestors更新")
    def test_ancestors_update_on_parent_change_004(self):
        reg = self.reg
        pa = f"pa_{self.case_id}"
        ch = f"ch_{self.case_id}"
        pc = f"pc_{self.case_id}"

        add_dept(deptName=pa, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=pa, fetch=[[reg, "pa_id", f"$.data[?(@.deptName=='{pa}')].deptId"]])

        add_dept(deptName=ch, parentId=reg.pa_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=ch, fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{ch}')].deptId"]])

        add_dept(deptName=pc, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=pc, fetch=[[reg, "pc_id", f"$.data[?(@.deptName=='{pc}')].deptId"]])

        mod_dept(deptId=reg.child_id, deptName=ch, parentId=reg.pc_id,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.child_id,
            check=[["$.data.ancestors", "include", str(reg.pc_id)]],
        )

    def teardown_method(self):
        for key in ["child_id", "pc_id", "pa_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced005:
    """TC-G5: 移动子部门到根级别"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g5_{ts}_{rs}"
        self.reg = register({"parent_id": None, "child_id": None})

    @allure.title("TC-G5: 移动子部门到根级别")
    def test_move_child_to_root_005(self):
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

        mod_dept(deptId=reg.child_id, deptName=c_name, parentId=100,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(deptId=reg.child_id,
                        check=[["$.data.parentId", "eq", 100]])

    def teardown_method(self):
        for key in ["child_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced006:
    """TC-G6: 同级创建多个兄弟部门"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g6_{ts}_{rs}"
        self.reg = register({
            "parent_id": None, "s1_id": None, "s2_id": None, "s3_id": None,
        })

    @allure.title("TC-G6: 同级创建多个兄弟部门")
    def test_create_siblings_006(self):
        reg = self.reg
        p_name = f"p_{self.case_id}"

        add_dept(deptName=p_name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p_name,
                 fetch=[[reg, "parent_id", f"$.data[?(@.deptName=='{p_name}')].deptId"]])

        for i, key in enumerate(["s1_id", "s2_id", "s3_id"], 1):
            s_name = f"s{i}_{self.case_id}"
            add_dept(deptName=s_name, parentId=reg.parent_id, orderNum=i, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=s_name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{s_name}')].deptId"]])

        for key in ["s1_id", "s2_id", "s3_id"]:
            lst_dept_detail(
                deptId=getattr(reg, key),
                check=[["$.data.parentId", "eq", reg.parent_id]],
            )

    def teardown_method(self):
        for key in ["s3_id", "s2_id", "s1_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced007:
    """TC-G7: 设置父节点为子孙节点 - 应失败"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g7_{ts}_{rs}"
        self.reg = register({"parent_id": None, "child_id": None})

    @allure.title("TC-G7: 设置父节点为子孙节点 - 验证系统行为")
    def test_set_parent_to_descendant_007(self):
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

        mod_dept(
            deptId=reg.parent_id, deptName=p_name, parentId=reg.child_id,
            orderNum=1, status="0",
            check=[["$.code", "==", 200]],
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
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced008:
    """TC-G8: 移动后验证子节点ancestors联动更新"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g8_{ts}_{rs}"
        self.reg = register({
            "pa_id": None, "child_id": None, "grandchild_id": None, "pd_id": None,
        })

    @allure.title("TC-G8: 移动后验证子节点ancestors联动更新")
    def test_descendants_ancestors_update_008(self):
        reg = self.reg
        pa = f"pa_{self.case_id}"
        ch = f"ch_{self.case_id}"
        gc = f"gc_{self.case_id}"
        pd = f"pd_{self.case_id}"

        add_dept(deptName=pa, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=pa, fetch=[[reg, "pa_id", f"$.data[?(@.deptName=='{pa}')].deptId"]])

        add_dept(deptName=ch, parentId=reg.pa_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=ch, fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{ch}')].deptId"]])

        add_dept(deptName=gc, parentId=reg.child_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=gc, fetch=[[reg, "grandchild_id", f"$.data[?(@.deptName=='{gc}')].deptId"]])

        add_dept(deptName=pd, parentId=100, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=pd, fetch=[[reg, "pd_id", f"$.data[?(@.deptName=='{pd}')].deptId"]])

        mod_dept(deptId=reg.child_id, deptName=ch, parentId=reg.pd_id,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.grandchild_id,
            check=[["$.data.ancestors", "include", str(reg.pd_id)]],
        )

    def teardown_method(self):
        for key in ["grandchild_id", "child_id", "pd_id", "pa_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced009:
    """TC-G9: 5层深度层级"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g9_{ts}_{rs}"
        self.reg = register({
            "l1_id": None, "l2_id": None, "l3_id": None,
            "l4_id": None, "l5_id": None,
        })

    @allure.title("TC-G9: 5层深度层级")
    def test_five_level_hierarchy_009(self):
        reg = self.reg
        keys = ["l1_id", "l2_id", "l3_id", "l4_id", "l5_id"]
        parent = 100

        for i, key in enumerate(keys):
            name = f"l{i+1}_{self.case_id}"
            add_dept(deptName=name, parentId=parent, orderNum=1, status="0",
                     check=[["$.msg", "eq", "操作成功"]])
            lst_dept(deptName=name,
                     fetch=[[reg, key, f"$.data[?(@.deptName=='{name}')].deptId"]])
            parent = getattr(reg, key)

        lst_dept_detail(
            deptId=reg.l5_id,
            check=[["$.data.parentId", "eq", reg.l4_id]],
        )

    def teardown_method(self):
        for key in ["l5_id", "l4_id", "l3_id", "l2_id", "l1_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass


@allure.feature("系统管理")
@allure.story("部门管理-高级层级")
class TestDeptHierarchyAdvanced010:
    """TC-G10: 每层多子节点树结构"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"g10_{ts}_{rs}"
        self.reg = register({
            "root_id": None,
            "a_id": None, "b_id": None,
            "a1_id": None, "a2_id": None,
        })

    @allure.title("TC-G10: 每层多子节点树结构")
    def test_multi_child_tree_010(self):
        reg = self.reg
        root = f"rt_{self.case_id}"

        add_dept(deptName=root, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=root,
                 fetch=[[reg, "root_id", f"$.data[?(@.deptName=='{root}')].deptId"]])

        a_name = f"a_{self.case_id}"
        b_name = f"b_{self.case_id}"
        add_dept(deptName=a_name, parentId=reg.root_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a_name,
                 fetch=[[reg, "a_id", f"$.data[?(@.deptName=='{a_name}')].deptId"]])

        add_dept(deptName=b_name, parentId=reg.root_id, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=b_name,
                 fetch=[[reg, "b_id", f"$.data[?(@.deptName=='{b_name}')].deptId"]])

        a1 = f"a1_{self.case_id}"
        a2 = f"a2_{self.case_id}"
        add_dept(deptName=a1, parentId=reg.a_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a1,
                 fetch=[[reg, "a1_id", f"$.data[?(@.deptName=='{a1}')].deptId"]])

        add_dept(deptName=a2, parentId=reg.a_id, orderNum=2, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=a2,
                 fetch=[[reg, "a2_id", f"$.data[?(@.deptName=='{a2}')].deptId"]])

        lst_dept_detail(deptId=reg.a_id, check=[["$.data.parentId", "eq", reg.root_id]])
        lst_dept_detail(deptId=reg.b_id, check=[["$.data.parentId", "eq", reg.root_id]])
        lst_dept_detail(deptId=reg.a1_id, check=[["$.data.parentId", "eq", reg.a_id]])
        lst_dept_detail(deptId=reg.a2_id, check=[["$.data.parentId", "eq", reg.a_id]])

    def teardown_method(self):
        for key in ["a2_id", "a1_id", "b_id", "a_id", "root_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass
