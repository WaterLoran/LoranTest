# coding: utf-8
"""
角色管理 - 查询与筛选测试 (I类 14个用例)
每个依赖角色数据的用例自建专属数据，teardown 清理。
"""
import allure
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_query_filter"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


@allure.feature("系统管理")
@allure.story("角色管理-查询筛选")
class TestRoleQueryFilter:
    def setup_method(self):
        self.reg = register({"role_id": None})

    def teardown_method(self):
        if getattr(self.reg, "role_id", None):
            try:
                rmv_role(role_id=self.reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")

    @allure.title("I01: 按角色名称模糊查询")
    def test_lst_role_by_name_like(self):
        rname = _uid("I01")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            roleName=rname[:10],
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("I02: 按权限字符模糊查询")
    def test_lst_role_by_key_like(self):
        rname = _uid("I02")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            roleKey=rname[:10],
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("I03: 按状态筛选")
    def test_lst_role_by_status(self):
        rname = _uid("I03")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="0")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(status="0", roleName=rname, check=[["$.code", "eq", 200], ["$.total", ">", 0]])
        lst_role(status="1", check=[["$.code", "eq", 200]])

    @allure.title("I04: 按创建时间起始查询")
    def test_lst_role_by_begin_time(self):
        rname = _uid("I04")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            beginTime="2020-01-01",
            endTime="",
            check=[["$.code", "eq", 200]],
        )

    @allure.title("I05: 按创建时间结束查询")
    def test_lst_role_by_end_time(self):
        rname = _uid("I05")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            beginTime="",
            endTime="2030-12-31",
            check=[["$.code", "eq", 200]],
        )

    @allure.title("I06: 按时间范围查询")
    def test_lst_role_by_time_range(self):
        rname = _uid("I06")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            beginTime="2020-01-01",
            endTime="2030-12-31",
            check=[["$.code", "eq", 200]],
        )

    @allure.title("I07: 分页-第1页")
    def test_lst_role_page_first(self):
        lst_role(
            pageNum=1,
            pageSize=10,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("I08: 分页-第2页")
    def test_lst_role_page_second(self):
        lst_role(
            pageNum=2,
            pageSize=10,
            check=[["$.code", "eq", 200]],
        )

    @allure.title("I09: 自定义pageSize")
    def test_lst_role_custom_page_size(self):
        lst_role(
            pageNum=1,
            pageSize=20,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("I10: 多条件组合查询")
    def test_lst_role_multi_condition(self):
        rname = _uid("I10")
        add_role(roleName=rname, roleKey=rname, roleSort=1, status="0")
        lst_role(
            roleName=rname,
            fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
        )
        lst_role(
            pageNum=1,
            pageSize=10,
            status="0",
            roleName=rname,
            check=[["$.code", "eq", 200], ["$.total", ">", 0]],
        )

    @allure.title("I11: 查询不存在的名称")
    def test_lst_role_name_not_exist(self):
        lst_role(
            roleName="__nonexistent_role_name_xyz_123__",
            check=[["$.code", "eq", 200], ["$.total", "eq", 0]],
        )

    @allure.title("I12: 角色下拉选项")
    def test_lst_role_option_select(self):
        lst_role_option_select(
            check=[["$.code", "eq", 200], ["$.data", "exist", True]],
        )

    @allure.title("I13: 列表默认排序验证")
    def test_lst_role_default_order(self):
        lst_role(
            pageNum=1,
            pageSize=100,
            check=[["$.code", "eq", 200], ["$.rows", "exist", True]],
        )

    @allure.title("I14: 角色ID精确查询")
    def test_lst_role_by_id(self):
        rname = _uid("I14")
        add_role(roleName=rname, roleKey=rname, roleSort=1)
        lst_role(roleName=rname, fetch=[self.reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"])
        lst_role(
            roleId=self.reg.role_id,
            check=[
                ["$.code", "eq", 200],
                [f"$.rows[?(@.roleId=={self.reg.role_id})]", "exist", True],
            ],
        )
