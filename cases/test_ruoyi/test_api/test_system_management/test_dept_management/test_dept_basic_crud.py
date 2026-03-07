#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部门管理 - 基础 CRUD 测试 (TC-A1~A6)
API 返回部门列表在 $.data，非 $.rows。
"""

import allure
import time
import random
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理")
class TestDeptBasicCRUD:
    """部门基础 CRUD 测试"""

    def setup_method(self):
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        self.dept_name = f"dept_test_{timestamp}_{random_suffix}"
        self.reg = register({"dept_id": None})

    def teardown_method(self):
        if self.reg.dept_id:
            try:
                rmv_dept(deptId=self.reg.dept_id)
            except Exception as e:
                print(f"清理部门失败 {self.reg.dept_id}: {e}")
        print("测试数据清理完成")

    @allure.title("TC-A1: 创建部门 - 正常流程")
    def test_create_dept(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            leader="测试负责人",
            phone="13800138000",
            email="test@example.com",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )

    @allure.title("TC-A2: 查询部门列表")
    def test_list_dept(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
            check=[
                [f"$.data[?(@.deptName=='{self.dept_name}')].deptName", "eq", self.dept_name],
                [f"$.data[?(@.deptName=='{self.dept_name}')].orderNum", "eq", 1],
                [f"$.data[?(@.deptName=='{self.dept_name}')].status", "eq", "0"],
            ],
        )
        assert self.reg.dept_id is not None

    @allure.title("TC-A3: 查询部门详情")
    def test_lst_dept_detail(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=2,
            status="0",
            leader="详情测试负责人",
            phone="13900139000",
            email="detail@example.com",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        lst_dept_detail(
            deptId=self.reg.dept_id,
            fetch=[
                [self.reg, "fetched_name", "$.data.deptName"],
                [self.reg, "fetched_order_num", "$.data.orderNum"],
                [self.reg, "fetched_status", "$.data.status"],
                [self.reg, "fetched_leader", "$.data.leader"],
                [self.reg, "fetched_phone", "$.data.phone"],
                [self.reg, "fetched_email", "$.data.email"],
            ],
            check=[
                ["$.code", "==", 200],
                ["$.data.deptName", "eq", self.dept_name],
                ["$.data.orderNum", "eq", 2],
                ["$.data.status", "eq", "0"],
                ["$.data.leader", "eq", "详情测试负责人"],
                ["$.data.phone", "eq", "13900139000"],
                ["$.data.email", "eq", "detail@example.com"],
            ],
        )

    @allure.title("TC-A4: 更新部门")
    def test_update_dept(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            leader="原始负责人",
            phone="13700137000",
            email="original@example.com",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        # 部门名称最多30字符
        updated_name = f"upd_{int(time.time())}_{random.randint(100, 999)}"
        mod_dept(
            deptId=self.reg.dept_id,
            deptName=updated_name,
            parentId=100,
            orderNum=3,
            status="1",
            leader="更新后的负责人",
            phone="13600136000",
            email="updated@example.com",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept_detail(
            deptId=self.reg.dept_id,
            check=[
                ["$.code", "==", 200],
                ["$.data.deptName", "eq", updated_name],
                ["$.data.orderNum", "eq", 3],
                ["$.data.status", "eq", "1"],
                ["$.data.leader", "eq", "更新后的负责人"],
                ["$.data.phone", "eq", "13600136000"],
                ["$.data.email", "eq", "updated@example.com"],
            ],
        )

    @allure.title("TC-A5: 删除部门")
    def test_delete_dept(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        rmv_dept(
            deptId=self.reg.dept_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        self.reg.dept_id = None

    @allure.title("TC-A6: 完整生命周期")
    def test_dept_lifecycle(self):
        add_dept(
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="0",
            leader="生命周期测试",
            phone="13400134000",
            email="lifecycle@example.com",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept(
            deptName=self.dept_name,
            fetch=[
                [self.reg, "dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        lst_dept_detail(
            deptId=self.reg.dept_id,
            check=[
                ["$.code", "==", 200],
                ["$.data.deptName", "eq", self.dept_name],
            ],
        )
        updated_name = f"upd_{int(time.time())}_{random.randint(100, 999)}"
        mod_dept(
            deptId=self.reg.dept_id,
            deptName=updated_name,
            parentId=100,
            orderNum=2,
            leader="更新后的生命周期测试",
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        lst_dept_detail(
            deptId=self.reg.dept_id,
            check=[
                ["$.data.deptName", "eq", updated_name],
                ["$.data.leader", "eq", "更新后的生命周期测试"],
            ],
        )
        rmv_dept(
            deptId=self.reg.dept_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
        self.reg.dept_id = None
        print("完整生命周期测试通过")
