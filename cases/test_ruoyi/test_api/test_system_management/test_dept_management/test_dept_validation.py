#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部门管理 - 校验与边界测试 (TC-D1~D5, TC-E1~E3)
- 名称唯一性、字段长度、格式、必填项
- 列表接口返回在 $.data，非 $.rows
"""

import allure
import time
import random
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理")
class TestDeptValidation:
    """部门校验与边界测试"""

    def setup_method(self):
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        self.dept_name = f"dept_val_{timestamp}_{random_suffix}"
        self.reg = register({"dept_id": None, "parent_dept_id": None})

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception as e:
                print(f"清理部门失败 {self.reg.dept_id}: {e}")
        if self.reg.parent_dept_id:
            try:
                rmv_dept(deptId=self.reg.parent_dept_id)
            except Exception as e:
                print(f"清理父部门失败 {self.reg.parent_dept_id}: {e}")
        print("测试数据清理完成")

    @allure.title("TC-D1: 同父部门下部门名称重复 - 应失败")
    def test_duplicate_dept_name(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=2,
            status="0",
            check=[
                ["$.code", "!=", 200],
                ["$.msg", "include", "部门名称已存在"],
            ],
        )

    @allure.title("TC-D2: 部门名称超过30字符 - 应失败")
    def test_dept_name_length(self):
        long_name = "a" * 40
        add_dept(
            deptName=long_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("TC-D3: 联系电话超过11位 - 应失败")
    def test_phone_length(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        mod_dept(
            deptId=self.reg.dept_id,
            deptName=f"updated_{self.dept_name}",
            parentId=100,
            orderNum=1,
            status="0",
            phone="13800138000123",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("TC-D4: 邮箱格式非法 - 应失败")
    def test_email_format(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        mod_dept(
            deptId=self.reg.dept_id,
            deptName=f"updated_{self.dept_name}",
            parentId=100,
            orderNum=1,
            status="0",
            email="invalid-email",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("TC-D5: 必填项缺失 - 应失败")
    def test_missing_required_fields(self):
        add_dept(
            deptName="",
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.code", "!=", 200]],
        )

    @allure.title("TC-E1: 查询不存在的部门")
    def test_query_nonexistent_dept(self):
        nonexistent_id = 999999
        # 若依可能返回 200（无 data 或 data 为空）或返回非 200；此处仅校验接口不抛错
        lst_dept_detail(
            deptId=nonexistent_id,
            check=[["$.code", "==", 200]],
        )

    @allure.title("TC-E2: 部门名称含特殊字符")
    def test_special_characters_in_name(self):
        # 名称≤30字符且含中文与特殊字符
        special_name = f"测@#_{int(time.time()) % 10000}"
        add_dept(
            deptName=special_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        # 特殊字符会破坏 JSONPath filter 中的 @/# 语法，
        # 用 API 的 deptName 参数做模糊匹配后取第一条结果
        lst_dept(
            deptName=special_name,
            fetch=[
                [self.reg, "dept_id", "$.data[0].deptId"],
            ],
        )

    @allure.title("TC-E3: 无筛选条件返回全部部门列表")
    def test_empty_filter_returns_all(self):
        lst_dept(
            check=[
                ["$.code", "==", 200],
                ["$.data", "exist", True],
            ],
        )
