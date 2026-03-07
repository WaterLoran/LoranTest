#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岗位管理 - 唯一性约束测试 (TC-G01~TC-G12)
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
class TestPostUniqueness(object):
    """岗位名称、编码唯一性"""

    def setup_method(self):
        self.reg = register({"position_id": None, "position_id2": None})

    def _gen(self, case_id):
        ts = int(time.time())
        rnd = random.randint(1000, 9999)
        self.post_name = f"{case_id}_{ts}_{rnd}"
        self.post_code = f"{case_id}_c_{ts}_{rnd}"

    def teardown_method(self):
        for key in ("position_id", "position_id2"):
            pid = getattr(self.reg, key, None)
            if isinstance(pid, list) and pid:
                pid = pid[0]
            if pid:
                try:
                    rmv_position(positionId=pid)
                except Exception:
                    pass

    @allure.title("TC-G01: 新增重复岗位名称")
    def test_add_duplicate_name(self):
        self._gen("TC_G01")
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
        code2 = f"TC_G01_dup_{int(time.time())}"
        add_position(
            positionName=self.post_name,
            positionCode=code2,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称已存在"]],
        )

    @allure.title("TC-G02: 新增重复岗位编码")
    def test_add_duplicate_code(self):
        self._gen("TC_G02")
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
        name2 = f"TC_G02_dup_{int(time.time())}"
        add_position(
            positionName=name2,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码已存在"]],
        )

    @allure.title("TC-G03: 修改为已存在名称")
    def test_mod_to_existing_name(self):
        self._gen("TC_G03")
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
        ts = int(time.time())
        name2 = f"TC_G03_en_{ts}"
        code2 = f"TC_G03_ec_{ts}"
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        mod_position(
            positionId=_pid(self.reg),
            positionName=name2,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称已存在"]],
        )

    @allure.title("TC-G04: 修改为已存在编码")
    def test_mod_to_existing_code(self):
        self._gen("TC_G04")
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
        ts = int(time.time())
        name2 = f"TC_G04_en2_{ts}"
        code2 = f"TC_G04_ec2_{ts}"
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        mod_position(
            positionId=_pid(self.reg),
            positionName=self.post_name,
            positionCode=code2,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码已存在"]],
        )

    @allure.title("TC-G05: 名称唯一编码不同可新增")
    def test_name_unique_code_diff_ok(self):
        self._gen("TC_G05")
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
        ts = int(time.time())
        name2 = f"TC_G05_dn_{ts}"
        code2 = f"TC_G05_dc_{ts}"
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        pid2 = self.reg.position_id2[0] if isinstance(self.reg.position_id2, list) else self.reg.position_id2
        if pid2:
            rmv_position(positionId=pid2)
        self.reg.position_id2 = None

    @allure.title("TC-G06: 编码唯一名称不同可新增")
    def test_code_unique_name_diff_ok(self):
        self._gen("TC_G06")
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
        ts = int(time.time())
        name2 = f"TC_G06_n2_{ts}"
        code2 = f"TC_G06_c2_{ts}"
        add_position(positionName=name2, positionCode=code2, postSort=1, check=[["$.code", "eq", 200]])
        lst_position(postName=name2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postName=='{name2}')].postId"]])
        pid2 = self.reg.position_id2[0] if isinstance(self.reg.position_id2, list) else self.reg.position_id2
        if pid2:
            rmv_position(positionId=pid2)
        self.reg.position_id2 = None

    @allure.title("TC-G07: 修改保持自身名称")
    def test_mod_keep_own_name(self):
        self._gen("TC_G07")
        add_position(
            positionName=self.post_name,
            positionCode=self.post_code,
            postSort=1,
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
            postSort=1,
            remark="新备注",
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.remark", "eq", "新备注"]])

    @allure.title("TC-G08: 修改保持自身编码")
    def test_mod_keep_own_code(self):
        self._gen("TC_G08")
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
            postSort=99,
            check=[["$.code", "eq", 200]],
        )
        lst_position_detail(positionId=_pid(self.reg), check=[["$.data.postSort", "eq", 99]])

    @allure.title("TC-G09: 同名称不同编码两条")
    def test_same_name_diff_code_reject(self):
        self._gen("TC_G09")
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
        code2 = f"TC_G09_c2_{int(time.time())}"
        add_position(
            positionName=self.post_name,
            positionCode=code2,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位名称已存在"]],
        )

    @allure.title("TC-G10: 同编码不同名称不允许")
    def test_same_code_diff_name_reject(self):
        self._gen("TC_G10")
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
        name2 = f"TC_G10_n2_{int(time.time())}"
        add_position(
            positionName=name2,
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 500], ["$.msg", "include", "岗位编码已存在"]],
        )

    @allure.title("TC-G11: 名称大小写是否区分")
    def test_name_case_sensitive(self):
        self._gen("TC_G11")
        ts = int(time.time())
        add_position(
            positionName=f"TC_G11_AbcName_{ts}",
            positionCode=self.post_code,
            postSort=1,
            check=[["$.code", "eq", 200]],
        )
        lst_position(
            postCode=self.post_code,
            fetch=[[self.reg, "position_id", f"$.rows[?(@.postCode=='{self.post_code}')].postId"]],
        )
        code2 = f"TC_G11_c2_{ts}"
        add_position(
            positionName=f"TC_G11_abcname_{ts}",
            positionCode=code2,
            postSort=1,
            check=[["$.code", "in", [200, 500]]],
        )
        try:
            lst_position(postCode=code2, fetch=[[self.reg, "position_id2", f"$.rows[?(@.postCode=='{code2}')].postId"]])
            pid2 = self.reg.position_id2
            if isinstance(pid2, list) and pid2:
                pid2 = pid2[0]
            if pid2:
                rmv_position(positionId=pid2)
        except Exception:
            pass
        self.reg.position_id2 = None

    @allure.title("TC-G12: 删除后同名可再创建")
    def test_after_delete_same_name_ok(self):
        self._gen("TC_G12")
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
        rmv_position(positionId=_pid(self.reg), check=[["$.code", "eq", 200]])
        self.reg.position_id = None
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
