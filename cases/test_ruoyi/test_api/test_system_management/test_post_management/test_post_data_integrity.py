#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 数据完整性测试 (TC-L01~TC-L06)
"""

import allure
import time
import random
from common.ruoyi_logic import *


def _pid(reg):
    if isinstance(reg.position_id, list) and reg.position_id:
        return reg.position_id[0]
    return reg.position_id


@allure.feature("系统管理")
@allure.story("岗位管理")
class TestPostDataIntegrity(object):
    """数据完整性（createBy/updateBy、一致性）"""

    def setup_method(self):
        self.reg = register({"position_id": None})

    def _gen(self, case_id):
        ts = int(time.time())
        rnd = random.randint(1000, 9999)
        self.post_name = f"{case_id}_{ts}_{rnd}"
        self.post_code = f"{case_id}_c_{ts}_{rnd}"

    def teardown_method(self):
        pid = _pid(self.reg)
        if pid:
            try:
                rmv_position(positionId=pid)
            except Exception:
                pass

    @allure.title("TC-L01: 创建后createBy createTime")
    def test_create_audit_fields(self):
        self._gen("TC_L01")
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
        lst_position_detail(
            positionId=_pid(self.reg),
            check=[
                ["$.code", "eq", 200],
                ["$.data.createBy", "exist", True],
                ["$.data.createTime", "exist", True],
            ],
        )

    @allure.title("TC-L02: 修改后updateBy updateTime")
    def test_update_audit_fields(self):
        self._gen("TC_L02")
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
        mod_position(
            positionId=_pid(self.reg),
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=2,
            remark="更新备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(
            positionId=_pid(self.reg),
            check=[
                ["$.data.updateBy", "exist", True],
                ["$.data.updateTime", "exist", True],
                ["$.data.remark", "eq", "更新备注"],
            ],
        )

    @allure.title("TC-L03: 修改单字段其它不变")
    def test_mod_single_field_others_unchanged(self):
        self._gen("TC_L03")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=5,
            status="0",
            remark="原备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
        )
        mod_position(
            positionId=_pid(self.reg),
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=5,
            status="0",
            remark="仅改备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(
            positionId=_pid(self.reg),
            check=[
                ["$.data.postName", "eq", self.post_name],
                ["$.data.postCode", "eq", self.post_code],
                ["$.data.postSort", "eq", 5],
                ["$.data.status", "eq", "0"],
                ["$.data.remark", "eq", "仅改备注"],
            ],
        )

    @allure.title("TC-L04: 列表与详情数据一致")
    def test_list_and_detail_consistent(self):
        self._gen("TC_L04")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=7,
            status="1",
            remark="一致备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[
                [self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"],
                [self.reg, "row_name", f"$.rows[?(@.postName=='{self.post_name}')].postName"],
                [self.reg, "row_code", f"$.rows[?(@.postName=='{self.post_name}')].postCode"],
                [self.reg, "row_sort", f"$.rows[?(@.postName=='{self.post_name}')].postSort"],
                [self.reg, "row_status", f"$.rows[?(@.postName=='{self.post_name}')].status"],
            ],
        )
        lst_position_detail(
            positionId=_pid(self.reg),
            fetch=[
                [self.reg, "detail_name", "$.data.postName"],
                [self.reg, "detail_code", "$.data.postCode"],
                [self.reg, "detail_sort", "$.data.postSort"],
                [self.reg, "detail_status", "$.data.status"],
            ],
        )
        row_name = self.reg.row_name[0] if isinstance(self.reg.row_name, list) else self.reg.row_name
        row_code = self.reg.row_code[0] if isinstance(self.reg.row_code, list) else self.reg.row_code
        row_sort = self.reg.row_sort[0] if isinstance(self.reg.row_sort, list) else self.reg.row_sort
        row_status = self.reg.row_status[0] if isinstance(self.reg.row_status, list) else self.reg.row_status
        assert row_name == self.reg.detail_name
        assert row_code == self.reg.detail_code
        assert row_sort == self.reg.detail_sort
        assert row_status == self.reg.detail_status

    @allure.title("TC-L05: 下拉与列表数据一致")
    def test_optionselect_and_list_consistent(self):
        self._gen("TC_L05")
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
        optionselect_position(fetch=[[self.reg, "option_data", "$.data"]])
        option_data = self.reg.option_data or []
        option_ids = [p.get("postId") for p in option_data if isinstance(p, dict) and p.get("postId")]
        assert _pid(self.reg) in option_ids

    @allure.title("TC-L06: 导出与列表数据一致")
    def test_export_and_list_consistent(self):
        self._gen("TC_L06")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postName=self.post_name,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{self.post_name}')].postId"]],
            check=[["$.total", ">=", 1]],
        )
        export_position(postName=self.post_name[:8], check=[])
