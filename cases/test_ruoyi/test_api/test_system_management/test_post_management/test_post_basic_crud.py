#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 基础 CRUD 测试 (TC-A01~TC-A20)
API 列表返回 $.rows，分页 total 在 $.total。
"""

import allure
import time
import random
from common.ruoyi_logic import *


def _post_id(reg):
    """从 register 取单个岗位 ID（fetch 可能返回列表）"""
    pid = reg.position_id
    if isinstance(pid, list) and pid:
        return pid[0]
    return pid


@allure.feature("系统管理")
@allure.story("岗位管理")
class TestPostBasicCRUD(object):
    """岗位基础 CRUD 测试"""

    def setup_method(self):
        self.reg = register({"position_id": None})

    def _gen(self, case_id):
        ts = int(time.time())
        rnd = random.randint(1000, 9999)
        self.post_name = f"{case_id}_{ts}_{rnd}"
        self.post_code = f"{case_id}_c_{ts}_{rnd}"

    def teardown_method(self):
        pid = _post_id(self.reg)
        if pid:
            try:
                rmv_position(positionId=pid)
            except Exception:
                pass

    @allure.title("TC-A01: 创建岗位-全部字段")
    def test_create_post_all_fields(self):
        self._gen("TC_A01")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            remark="备注A",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position(
            postName=self.post_name,
            check=[
                [f"$.rows[?(@.postName=='{self.post_name}')].postCode", "eq", self.post_code],
                [f"$.rows[?(@.postName=='{self.post_name}')].postSort", "eq", 1],
                [f"$.rows[?(@.postName=='{self.post_name}')].status", "eq", "0"],
            ],
        )

    @allure.title("TC-A02: 创建岗位-仅必填")
    def test_create_post_required_only(self):
        self._gen("TC_A02")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(
            positionId=_post_id(self.reg),
            check=[
                ["$.code", "eq", 200],
                ["$.data.status", "eq", "0"],
            ],
        )

    @allure.title("TC-A03: 查询列表-无筛选")
    def test_list_no_filter(self):
        lst_position(pageNum=1, pageSize=10, check=[["$.code", "eq", 200], ["$.rows", "exist", True]])
        lst_position(check=[["$.total", ">=", 0]])

    @allure.title("TC-A04: 查询列表-按名称")
    def test_list_by_name(self):
        self._gen("TC_A04")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-A05: 查询列表-按编码")
    def test_list_by_code(self):
        self._gen("TC_A05")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postCode=self.post_code,
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-A06: 查询列表-按状态")
    def test_list_by_status(self):
        lst_position(status="0", check=[["$.code", "eq", 200]])
        lst_position(status="1", check=[["$.code", "eq", 200]])

    @allure.title("TC-A07: 查询列表-组合条件")
    def test_list_combined_filter(self):
        self._gen("TC_A07")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            status="0",
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-A08: 查询岗位详情")
    def test_post_detail(self):
        self._gen("TC_A08")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=2,
            status="0",
            remark="详情备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(
            positionId=_post_id(self.reg),
            check=[
                ["$.code", "eq", 200],
                ["$.data.postName", "eq", self.post_name],
                ["$.data.postCode", "eq", self.post_code],
                ["$.data.postSort", "eq", 2],
                ["$.data.status", "eq", "0"],
                ["$.data.remark", "eq", "详情备注"],
            ],
        )

    @allure.title("TC-A09: 修改岗位-全部字段")
    def test_update_post_all_fields(self):
        self._gen("TC_A09")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            remark="原备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        ts = int(time.time())
        new_name = f"TC_A09_upd_{ts}_{random.randint(100, 999)}"
        new_code = f"TC_A09_uc_{ts}_{random.randint(100, 999)}"
        mod_position(
            positionId=_post_id(self.reg),
            positionName=new_name,
            positionCode=new_code,
            postSort=10,
            status="1",
            remark="新备注",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]],
        )
        lst_position_detail(
            positionId=_post_id(self.reg),
            check=[
                ["$.data.postName", "eq", new_name],
                ["$.data.postCode", "eq", new_code],
                ["$.data.postSort", "eq", 10],
                ["$.data.status", "eq", "1"],
                ["$.data.remark", "eq", "新备注"],
            ],
        )

    @allure.title("TC-A10: 修改岗位-部分字段")
    def test_update_post_partial(self):
        self._gen("TC_A10")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            remark="原备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        only_name = f"TC_A10_on_{int(time.time())}"
        mod_position(
            positionId=_post_id(self.reg),
            positionName=only_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            remark="原备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(
            positionId=_post_id(self.reg),
            check=[
                ["$.data.postName", "eq", only_name],
                ["$.data.postCode", "eq", self.post_code],
                ["$.data.postSort", "eq", 1],
            ],
        )

    @allure.title("TC-A11: 删除单个岗位")
    def test_delete_single_post(self):
        self._gen("TC_A11")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        pid = _post_id(self.reg)
        rmv_position(positionId=pid, check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]])
        self.reg.position_id = None
        lst_position_detail(positionId=pid, check=[["$.code", "in", [200, 500]]])

    @allure.title("TC-A12: 批量删除岗位")
    def test_batch_delete_posts(self):
        ts = int(time.time())
        name1 = f"TC_A12_b1_{ts}_{random.randint(100, 999)}"
        code1 = f"TC_A12_bc1_{ts}_{random.randint(100, 999)}"
        name2 = f"TC_A12_b2_{ts}_{random.randint(100, 999)}"
        code2 = f"TC_A12_bc2_{ts}_{random.randint(100, 999)}"
        add_position(positionName=name1, positionCode=code1, postSort=1, check=[["$.code", "eq", 200]])
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name1, fetch=[[self.reg, "id1", f"$.rows[?(@.postName=='{name1}')].postId"]])
        lst_position(postName=name2, fetch=[[self.reg, "id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        id1 = self.reg.id1[0] if isinstance(self.reg.id1, list) else self.reg.id1
        id2 = self.reg.id2[0] if isinstance(self.reg.id2, list) else self.reg.id2
        rmv_position(positionId=f"{id1},{id2}", check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-A13: 获取下拉选项")
    def test_optionselect(self):
        optionselect_position(check=[["$.code", "eq", 200], ["$.data", "exist", True]])

    @allure.title("TC-A14: 导出岗位-无筛选")
    def test_export_no_filter(self):
        export_position(check=[])

    @allure.title("TC-A15: 导出岗位-有筛选")
    def test_export_with_filter(self):
        export_position(postName="TC_A15", status="0", check=[])

    @allure.title("TC-A16: 完整生命周期")
    def test_post_lifecycle(self):
        self._gen("TC_A16")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            status="0",
            remark="生命周期",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        lst_position_detail(positionId=_post_id(self.reg), check=[["$.data.postName", "eq", self.post_name]])
        new_name = f"TC_A16_lf_{int(time.time())}"
        mod_position(
            positionId=_post_id(self.reg),
            positionName=new_name,
            positionCode=self.post_code,
            postSort=2,
            remark="更新后备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_post_id(self.reg), check=[["$.data.postName", "eq", new_name]])
        rmv_position(positionId=_post_id(self.reg), check=[["$.msg", "eq", "操作成功"]])
        self.reg.position_id = None

    @allure.title("TC-A17: 创建后立即查询")
    def test_create_then_list(self):
        self._gen("TC_A17")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            check=[["$.code", "eq", 200], ["$.total", ">=", 1]],
        )

    @allure.title("TC-A18: 修改后立即查询")
    def test_update_then_detail(self):
        self._gen("TC_A18")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        new_name = f"TC_A18_ui_{int(time.time())}"
        mod_position(
            positionId=_post_id(self.reg),
            positionName=new_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_post_id(self.reg), check=[["$.data.postName", "eq", new_name]])

    @allure.title("TC-A19: 删除后查询详情应失败")
    def test_detail_after_delete(self):
        self._gen("TC_A19")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        pid = _post_id(self.reg)
        rmv_position(positionId=pid, check=[["$.code", "eq", 200]])
        self.reg.position_id = None
        lst_position_detail(positionId=pid, check=[["$.code", "in", [200, 500]]])

    @allure.title("TC-A20: 空列表分页")
    def test_list_empty_result(self):
        lst_position(
            postName="TC_A20_不可能存在的岗位名称_xyz_999999",
            pageNum=1,
            pageSize=10,
            check=[["$.code", "eq", 200], ["$.total", "eq", 0], ["$.rows", "exist", True]],
        )
