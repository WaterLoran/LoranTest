#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 删除约束测试 (TC-H01~TC-H08)
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
class TestPostDeleteConstraints(object):
    """删除岗位约束（已分配不可删等）"""

    def setup_method(self):
        self.reg = register({"position_id": None, "position_id2": None, "user_id": None})

    def _gen(self, case_id):
        ts = int(time.time())
        rnd = random.randint(1000, 9999)
        self.post_name = f"{case_id}_{ts}_{rnd}"
        self.post_code = f"{case_id}_c_{ts}_{rnd}"

    def teardown_method(self):
        uid = getattr(self.reg, "user_id", None)
        if isinstance(uid, list) and uid:
            uid = uid[0]
        if uid:
            try:
                rmv_user(userId=uid)
            except Exception:
                pass
        for key in ("position_id", "position_id2"):
            pid = getattr(self.reg, key, None)
            if isinstance(pid, list) and pid:
                pid = pid[0]
            if pid:
                try:
                    rmv_position(positionId=pid)
                except Exception:
                    pass

    @allure.title("TC-H01: 删除未分配岗位")
    def test_delete_unassigned(self):
        self._gen("TC_H01")
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
        rmv_position(positionId=_pid(self.reg), check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-H02: 删除已分配用户岗位应失败")
    def test_delete_assigned_fail(self):
        self._gen("TC_H02")
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
        pid = _pid(self.reg)
        ts = int(time.time())
        user_name = f"TC_H02_u_{ts}_{random.randint(100, 999)}"
        add_user(
            userName=user_name,
            nickName=user_name,
            password="admin123",
            postIds=[pid],
            roleIds=[2],
            deptId=100,
            check=[["$.code", "eq", 200]],
        )
        reg_u = register({"user_id": None})
        lst_user(
            userName=user_name,
            fetch=[[reg_u, "user_id", f"$.rows[?(@.userName=='{user_name}')].userId"]],
        )
        rmv_position(
            positionId=pid,
            check=[["$.code", "eq", 500], ["$.msg", "include", "已分配"]],
        )
        uid = reg_u.user_id
        if isinstance(uid, list) and uid:
            uid = uid[0]
        if uid and not isinstance(uid, bool):
            rmv_user(userId=uid)
        rmv_position(positionId=pid, check=[["$.code", "eq", 200]])
        self.reg.position_id = None

    @allure.title("TC-H03: 批量删除全未分配")
    def test_batch_delete_all_unassigned(self):
        ts = int(time.time())
        name1 = f"TC_H03_b1_{ts}_{random.randint(100, 999)}"
        name2 = f"TC_H03_b2_{ts}_{random.randint(100, 999)}"
        code1 = f"TC_H03_bc1_{ts}_{random.randint(100, 999)}"
        code2 = f"TC_H03_bc2_{ts}_{random.randint(100, 999)}"
        add_position(positionName=name1, positionCode=code1, postSort=1, check=[["$.code", "eq", 200]])
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name1, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name1}')].postId"]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        id1 = _pid(self.reg)
        id2 = self.reg.position_id2[0] if isinstance(self.reg.position_id2, list) else self.reg.position_id2
        rmv_position(positionId=f"{id1},{id2}", check=[["$.msg", "eq", "操作成功"], ["$.code", "eq", 200]])
        self.reg.position_id = None
        self.reg.position_id2 = None

    @allure.title("TC-H04: 批量删除含已分配")
    def test_batch_delete_one_assigned(self):
        ts = int(time.time())
        name1 = f"TC_H04_ba1_{ts}_{random.randint(100, 999)}"
        name2 = f"TC_H04_ba2_{ts}_{random.randint(100, 999)}"
        code1 = f"TC_H04_bac1_{ts}_{random.randint(100, 999)}"
        code2 = f"TC_H04_bac2_{ts}_{random.randint(100, 999)}"
        add_position(positionName=name1, positionCode=code1, postSort=1, check=[["$.code", "eq", 200]])
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name1, fetch=[[self.reg, "position_id", f"$.rows[?(@.postName=='{name1}')].postId"]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        id1 = _pid(self.reg)
        id2 = self.reg.position_id2[0] if isinstance(self.reg.position_id2, list) else self.reg.position_id2
        user_name = f"TC_H04_u_{ts}_{random.randint(100, 999)}"
        add_user(
            userName=user_name,
            nickName=user_name,
            password="admin123",
            postIds=[id2],
            roleIds=[2],
            deptId=100,
            check=[["$.code", "eq", 200]],
        )
        reg_u = register({"user_id": None})
        lst_user(userName=user_name, fetch=[[reg_u, "user_id", f"$.rows[?(@.userName=='{user_name}')].userId"]])
        rmv_position(positionId=f"{id1},{id2}", check=[["$.code", "eq", 500], ["$.msg", "include", "已分配"]])
        uid = reg_u.user_id
        if isinstance(uid, list) and uid:
            uid = uid[0]
        if uid and not isinstance(uid, bool):
            rmv_user(userId=uid)
        rmv_position(positionId=id1, check=[["$.code", "eq", 200]])
        rmv_position(positionId=id2, check=[["$.code", "eq", 200]])
        self.reg.position_id = None
        self.reg.position_id2 = None

    @allure.title("TC-H05: 删除不存在ID")
    def test_delete_nonexistent_id(self):
        rmv_position(positionId=999999, check=[["$.code", "eq", 500]])

    @allure.title("TC-H06: 删除ID为0")
    def test_delete_id_zero(self):
        rmv_position(positionId=0, check=[["$.code", "!=", 200]])

    @allure.title("TC-H07: 删除负数ID")
    def test_delete_negative_id(self):
        rmv_position(positionId=-1, check=[["$.code", "!=", 200]])

    @allure.title("TC-H08: 删除非数字ID")
    def test_delete_non_numeric_id(self):
        lst_position_detail(positionId="abc", check=[["$.code", "!=", 200]])
        self.reg.position_id = None
