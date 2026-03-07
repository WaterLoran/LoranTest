# coding: utf-8
"""
部门管理 - 查询与筛选测试 (TC-K1~K10)
验证列表筛选、组合筛选、排除查询等场景。
"""
import time
import random
import allure
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter001:
    """TC-K1: 按精确名称筛选"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k1_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K1: 按精确名称筛选")
    def test_filter_by_exact_name_001(self):
        reg = self.reg
        name = f"ex_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept(
            deptName=name,
            check=[
                ["$.code", "==", 200],
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
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter002:
    """TC-K2: 按模糊名称筛选"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k2_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K2: 按模糊名称筛选")
    def test_filter_by_fuzzy_name_002(self):
        reg = self.reg
        name = f"fz_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept(
            deptName=f"fz_{self.case_id[:8]}",
            check=[["$.code", "==", 200], ["$.data", "exist", True]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter003:
    """TC-K3: 按status=0筛选"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k3_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K3: 按status=0筛选")
    def test_filter_by_status_normal_003(self):
        reg = self.reg
        name = f"sn_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept(
            status="0",
            check=[["$.code", "==", 200], ["$.data", "exist", True]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter004:
    """TC-K4: 按status=1筛选"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k4_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K4: 按status=1筛选")
    def test_filter_by_status_disabled_004(self):
        reg = self.reg
        name = f"sd_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept(
            status="1",
            check=[["$.code", "==", 200], [f"$.data[?(@.deptName=='{name}')]", "exist", True]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter005:
    """TC-K5: 组合筛选(名称+status=0)"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k5_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K5: 组合筛选(名称+status=0)")
    def test_combined_filter_name_status0_005(self):
        reg = self.reg
        name = f"cs0_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        lst_dept(
            deptName=name, status="0",
            check=[
                ["$.code", "==", 200],
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
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter006:
    """TC-K6: 组合筛选(名称+status=1)"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k6_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K6: 组合筛选(名称+status=1)")
    def test_combined_filter_name_status1_006(self):
        reg = self.reg
        name = f"cs1_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept(
            deptName=name, status="1",
            check=[
                ["$.code", "==", 200],
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
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter007:
    """TC-K7: 筛选结果为空"""

    def setup_method(self):
        pass

    @allure.title("TC-K7: 筛选结果为空")
    def test_filter_empty_result_007(self):
        nonexist_name = f"nonexist_{int(time.time())}_{random.randint(10000, 99999)}"
        lst_dept(
            deptName=nonexist_name,
            check=[["$.code", "==", 200]],
        )

    def teardown_method(self):
        pass


@allure.feature("系统管理")
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter008:
    """TC-K8: 更新后立即查询验证"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k8_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K8: 更新后立即查询验证")
    def test_query_after_update_008(self):
        reg = self.reg
        name = f"qu_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])

        new_name = f"uq_{self.case_id}"
        mod_dept(deptId=reg.dept_id, deptName=new_name, parentId=100,
                 orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept(
            deptName=new_name,
            check=[[f"$.data[?(@.deptName=='{new_name}')]", "exist", True]],
        )

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception:
                pass


@allure.feature("系统管理")
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter009:
    """TC-K9: 查询停用部门详情"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k9_{ts}_{rs}"
        self.reg = register({"dept_id": None})

    @allure.title("TC-K9: 查询停用部门详情")
    def test_query_disabled_dept_detail_009(self):
        reg = self.reg
        name = f"dd_{self.case_id}"

        add_dept(deptName=name, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=name,
                 fetch=[[reg, "dept_id", f"$.data[?(@.deptName=='{name}')].deptId"]])
        mod_dept(deptId=reg.dept_id, deptName=name, parentId=100,
                 orderNum=1, status="1",
                 check=[["$.msg", "eq", "操作成功"]])

        lst_dept_detail(
            deptId=reg.dept_id,
            check=[
                ["$.code", "==", 200],
                ["$.data.status", "eq", "1"],
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
@allure.story("部门管理-查询筛选")
class TestDeptQueryFilter010:
    """TC-K10: 排除查询验证子树完整排除"""

    def setup_method(self):
        ts = int(time.time()) % 100000
        rs = random.randint(100, 999)
        self.case_id = f"k10_{ts}_{rs}"
        self.reg = register({
            "parent_id": None, "child_id": None, "grandchild_id": None,
        })

    @allure.title("TC-K10: 排除查询验证子树完整排除")
    def test_exclude_full_subtree_010(self):
        reg = self.reg
        p = f"p_{self.case_id}"
        c = f"c_{self.case_id}"
        g = f"g_{self.case_id}"

        add_dept(deptName=p, parentId=100, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=p,
                 fetch=[[reg, "parent_id", f"$.data[?(@.deptName=='{p}')].deptId"]])

        add_dept(deptName=c, parentId=reg.parent_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=c,
                 fetch=[[reg, "child_id", f"$.data[?(@.deptName=='{c}')].deptId"]])

        add_dept(deptName=g, parentId=reg.child_id, orderNum=1, status="0",
                 check=[["$.msg", "eq", "操作成功"]])
        lst_dept(deptName=g,
                 fetch=[[reg, "grandchild_id", f"$.data[?(@.deptName=='{g}')].deptId"]])

        lst_dept_exclude(
            deptId=reg.parent_id,
            fetch=[[reg, "exclude_data", "$.data"]],
            check=[["$.code", "==", 200]],
        )
        if reg.exclude_data:
            ids = [d.get("deptId") for d in reg.exclude_data if isinstance(d, dict)]
            assert reg.parent_id not in ids, "父部门不应在排除列表中"
            assert reg.child_id not in ids, "子部门不应在排除列表中"
            assert reg.grandchild_id not in ids, "孙子部门不应在排除列表中"

    def teardown_method(self):
        for key in ["grandchild_id", "child_id", "parent_id"]:
            did = getattr(self.reg, key, None)
            if did:
                try:
                    rmv_dept(deptId=did)
                except Exception:
                    pass
