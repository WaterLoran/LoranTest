# coding: utf-8
"""
角色管理 - 基础 CRUD 测试 (A类 12个用例)
API 列表返回在 $.rows，分页 total 在 $.total。
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_basic_crud"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理")
class TestRoleBasicCRUD:
    """角色基础 CRUD 测试"""

    def setup_method(self):
        self.reg = register({"role_id": None, "role_id_2": None})

    def teardown_method(self):
        for key in ("role_id", "role_id_2"):
            rid = getattr(self.reg, key, None)
            if rid:
                try:
                    rmv_role(role_id=rid)
                except Exception as e:
                    print(f"清理角色失败 {rid}: {e}")

    @allure.title("A01: 新增角色-全部有效参数")
    def test_add_role_full_params(self):
        rname = _uid("A01")
        rkey = _uid("A01_key")
        add_role(
            roleName=rname,
            roleKey=rkey,
            roleSort=5,
            status="0",
            menuIds=[1, 100, 1000],
            deptIds=[],
            menuCheckStrictly=True,
            deptCheckStrictly=True,
            remark="全部参数备注",
            check=[["$.code", "eq", 200], ["$.msg", "eq", "操作成功"]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[
                [f"$.rows[?(@.roleName=='{rname}')].roleName", "eq", rname],
                [f"$.rows[?(@.roleName=='{rname}')].roleKey", "eq", rkey],
                [f"$.rows[?(@.roleName=='{rname}')].roleSort", "eq", 5],
                [f"$.rows[?(@.roleName=='{rname}')].remark", "eq", "全部参数备注"],
            ],
        )
        assert self.reg.role_id is not None

    @allure.title("A02: 新增角色-最少必填参数")
    def test_add_role_minimal_params(self):
        rname = _uid("A02")
        rkey = _uid("A02_key")
        add_role(
            roleName=rname,
            roleKey=rkey,
            roleSort=1,
            check=[["$.code", "eq", 200], ["$.msg", "eq", "操作成功"]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[
                [f"$.rows[?(@.roleName=='{rname}')].roleName", "eq", rname],
                [f"$.rows[?(@.roleName=='{rname}')].roleKey", "eq", rkey],
                [f"$.rows[?(@.roleName=='{rname}')].roleSort", "eq", 1],
            ],
        )
        assert self.reg.role_id is not None

    @allure.title("A03: 查询角色列表-默认分页")
    def test_lst_role_default_pagination(self):
        lst_role(
            pageNum=1,
            pageSize=10,
            check=[
                ["$.code", "eq", 200],
                ["$.msg", "eq", "查询成功"],
                ["$.rows", "exist", True],
                ["$.total", ">=", 0],
            ],
        )

    @allure.title("A04: 查询角色详情-有效ID")
    def test_lst_role_detail_valid_id(self):
        rname = _uid("A04")
        add_role(roleName=rname, roleKey=rname, roleSort=2)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role_detail(
            roleId=self.reg.role_id,
            check=[
                ["$.code", "eq", 200],
                ["$.data.roleId", "eq", self.reg.role_id],
                ["$.data.roleName", "eq", rname],
                ["$.data.roleKey", "eq", rname],
                ["$.data.roleSort", "eq", 2],
            ],
        )

    @allure.title("A05: 修改角色-全部字段")
    def test_mod_role_all_fields(self):
        rname = _uid("A05")
        add_role(roleName=rname, roleKey=rname, roleSort=3, remark="原备注")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        new_name = _uid("A05_new")
        new_key = _uid("A05_key_new")
        mod_role(
            roleId=self.reg.role_id,
            roleName=new_name,
            roleKey=new_key,
            roleSort=10,
            status="0",
            menuIds=[1, 100],
            remark="修改后备注",
            check=[["$.code", "eq", 200], ["$.msg", "eq", "操作成功"]],
        )
        lst_role_detail(
            roleId=self.reg.role_id,
            check=[
                ["$.data.roleName", "eq", new_name],
                ["$.data.roleKey", "eq", new_key],
                ["$.data.roleSort", "eq", 10],
                ["$.data.remark", "eq", "修改后备注"],
            ],
        )

    @allure.title("A06: 修改角色-部分字段")
    def test_mod_role_partial_fields(self):
        rname = _uid("A06")
        add_role(roleName=rname, roleKey=rname, roleSort=4, remark="原备注")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        mod_role(
            roleId=self.reg.role_id,
            roleName=rname,
            roleKey=rname,
            roleSort=8,
            remark="仅改排序和备注",
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(
            roleId=self.reg.role_id,
            check=[
                ["$.data.roleName", "eq", rname],
                ["$.data.roleSort", "eq", 8],
                ["$.data.remark", "eq", "仅改排序和备注"],
            ],
        )

    @allure.title("A07: 删除单个角色")
    def test_rmv_role_single(self):
        rname = _uid("A07")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        rmv_role(
            role_id=self.reg.role_id,
            check=[["$.code", "eq", 200], ["$.msg", "eq", "操作成功"]],
        )
        self.reg.role_id = None

    @allure.title("A08: 批量删除多个角色")
    def test_rmv_role_batch(self):
        r1 = _uid("A08_a")
        r2 = _uid("A08_b")
        add_role(roleName=r1, roleKey=r1, roleSort=1)
        add_role(roleName=r2, roleKey=r2, roleSort=2)
        lst_role(roleName=r1, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{r1}')].roleId"])
        lst_role(roleName=r2, fetch=[self.reg, "role_id_2", f"$.rows[?(@.roleName=='{r2}')].roleId"])
        rmv_role(
            role_id=f"{self.reg.role_id},{self.reg.role_id_2}",
            check=[["$.code", "eq", 200], ["$.msg", "eq", "操作成功"]],
        )
        self.reg.role_id = None
        self.reg.role_id_2 = None

    @allure.title("A09: 角色完整生命周期")
    def test_role_lifecycle(self):
        rname = _uid("A09")
        add_role(roleName=rname, roleKey=rname, roleSort=1, remark="生命周期")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.roleName", "eq", rname]])
        new_name = _uid("A09_upd")
        mod_role(
            roleId=self.reg.role_id,
            roleName=new_name,
            roleKey=new_name,
            roleSort=2,
            remark="更新后",
            check=[["$.code", "eq", 200]],
        )
        lst_role_detail(roleId=self.reg.role_id, check=[["$.data.roleName", "eq", new_name]])
        rmv_role(role_id=self.reg.role_id, check=[["$.code", "eq", 200]])
        self.reg.role_id = None

    @allure.title("A10: 新增角色带备注")
    def test_add_role_with_remark(self):
        rname = _uid("A10")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=1,
            remark="测试备注内容",
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].remark", "eq", "测试备注内容"]],
        )
        assert self.reg.role_id is not None

    @allure.title("A11: 新增角色-不同排序值")
    def test_add_role_different_sort(self):
        rname = _uid("A11")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=99,
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[[f"$.rows[?(@.roleName=='{rname}')].roleSort", "eq", 99]],
        )
        assert self.reg.role_id is not None

    @allure.title("A12: 查询角色下拉选项")
    def test_lst_role_option_select(self):
        lst_role_option_select(
            check=[
                ["$.code", "eq", 200],
                ["$.data", "exist", True],
            ],
        )
