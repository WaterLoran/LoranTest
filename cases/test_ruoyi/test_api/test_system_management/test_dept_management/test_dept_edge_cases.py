#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部门管理 - 边界与业务规则测试 (TC-B1~B5, TC-C1~C3)
- 父子关系、删除约束、状态规则
- 列表接口返回在 $.data，非 $.rows
"""

import allure
import time
import random
from common.ruoyi_logic import *


@allure.feature("系统管理")
@allure.story("部门管理")
class TestDeptEdgeCases:
    """部门边界与业务规则测试"""

    def setup_method(self):
        # 部门名称最多30字符，parent_/child_ 等前缀会加长，故用短后缀
        timestamp = int(time.time()) % 100000
        random_suffix = random.randint(100, 999)
        self.dept_name = f"e{timestamp}_{random_suffix}"
        self.reg = register({
            "parent_dept_id": None,
            "child_dept_id": None,
            "grandchild_dept_id": None,
        })

    def teardown_method(self):
        # 从下往上删除：孙子 -> 子 -> 父
        if self.reg.grandchild_dept_id:
            try:
                rmv_dept(deptId=self.reg.grandchild_dept_id)
            except Exception as e:
                print(f"清理孙子部门失败 {self.reg.grandchild_dept_id}: {e}")
        if self.reg.child_dept_id:
            try:
                rmv_dept(deptId=self.reg.child_dept_id)
            except Exception as e:
                print(f"清理子部门失败 {self.reg.child_dept_id}: {e}")
        if self.reg.parent_dept_id:
            try:
                rmv_dept(deptId=self.reg.parent_dept_id)
            except Exception as e:
                print(f"清理父部门失败 {self.reg.parent_dept_id}: {e}")
        print("测试数据清理完成")

    @allure.title("TC-B1: 创建子部门")
    def test_create_child_dept(self):
        parent_name = f"parent_{self.dept_name}"
        child_name = f"child_{self.dept_name}"
        add_dept(
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=parent_name,
            fetch=[
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{parent_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=child_name,
            fetch=[
                [self.reg, "child_dept_id", f"$.data[?(@.deptName=='{child_name}')].deptId"],
            ],
        )
        lst_dept_detail(
            deptId=self.reg.child_dept_id,
            check=[
                ["$.code", "==", 200],
                ["$.data.deptName", "eq", child_name],
                ["$.data.parentId", "eq", self.reg.parent_dept_id],
            ],
        )

    @allure.title("TC-B2: 多级层级")
    def test_multi_level_hierarchy(self):
        parent_name = f"parent_{self.dept_name}"
        child_name = f"child_{self.dept_name}"
        grandchild_name = f"grandchild_{self.dept_name}"
        add_dept(
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=parent_name,
            fetch=[
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{parent_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=child_name,
            fetch=[
                [self.reg, "child_dept_id", f"$.data[?(@.deptName=='{child_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=grandchild_name,
            parentId=self.reg.child_dept_id,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=grandchild_name,
            fetch=[
                [self.reg, "grandchild_dept_id", f"$.data[?(@.deptName=='{grandchild_name}')].deptId"],
            ],
        )
        lst_dept_detail(
            deptId=self.reg.grandchild_dept_id,
            check=[
                ["$.data.deptName", "eq", grandchild_name],
                ["$.data.parentId", "eq", self.reg.child_dept_id],
            ],
        )

    @allure.title("TC-B3: 删除有子部门的部门 - 应失败")
    def test_delete_dept_with_children(self):
        parent_name = f"parent_{self.dept_name}"
        child_name = f"child_{self.dept_name}"
        add_dept(
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=parent_name,
            fetch=[
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{parent_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=child_name,
            fetch=[
                [self.reg, "child_dept_id", f"$.data[?(@.deptName=='{child_name}')].deptId"],
            ],
        )
        rmv_dept(
            deptId=self.reg.parent_dept_id,
            check=[
                ["$.code", "!=", 200],
                ["$.msg", "include", "存在下级部门"],
            ],
        )
        rmv_dept(deptId=self.reg.child_dept_id, check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        self.reg.child_dept_id = None
        rmv_dept(deptId=self.reg.parent_dept_id, check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]])
        self.reg.parent_dept_id = None

    @allure.title("TC-B4: 设置父部门为自身 - 应失败")
    def test_set_parent_to_self(self):
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
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        mod_dept(
            deptId=self.reg.parent_dept_id,
            deptName=self.dept_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[
                ["$.code", "!=", 200],
                ["$.msg", "include", "上级部门不能是自己"],
            ],
        )

    @allure.title("TC-B5: 排除查询")
    def test_exclude_dept_query(self):
        parent_name = f"parent_exclude_{self.dept_name}"
        child_name = f"child_exclude_{self.dept_name}"
        add_dept(
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=parent_name,
            fetch=[
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{parent_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=child_name,
            fetch=[
                [self.reg, "child_dept_id", f"$.data[?(@.deptName=='{child_name}')].deptId"],
            ],
        )
        lst_dept_exclude(
            deptId=self.reg.parent_dept_id,
            fetch=[[self.reg, "exclude_data", "$.data"]],
            check=[["$.code", "==", 200]],
        )
        if self.reg.exclude_data:
            ids = [d.get("deptId") for d in self.reg.exclude_data if isinstance(d, dict)]
            assert self.reg.parent_dept_id not in ids
            assert self.reg.child_dept_id not in ids

    @allure.title("TC-C1: 停用部门")
    def test_disable_dept(self):
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
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        mod_dept(
            deptId=self.reg.parent_dept_id,
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="1",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept_detail(
            deptId=self.reg.parent_dept_id,
            check=[["$.data.status", "eq", "1"]],
        )

    @allure.title("TC-C2: 停用有启用子部门的部门 - 应失败")
    def test_disable_dept_with_enabled_children(self):
        parent_name = f"parent_disable_{self.dept_name}"
        child_name = f"child_disable_{self.dept_name}"
        add_dept(
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=parent_name,
            fetch=[
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{parent_name}')].deptId"],
            ],
        )
        add_dept(
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        lst_dept(
            deptName=child_name,
            fetch=[
                [self.reg, "child_dept_id", f"$.data[?(@.deptName=='{child_name}')].deptId"],
            ],
        )
        mod_dept(
            deptId=self.reg.parent_dept_id,
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="1",
            check=[
                ["$.code", "!=", 200],
                ["$.msg", "include", "该部门包含未停用的子部门"],
            ],
        )
        mod_dept(
            deptId=self.reg.child_dept_id,
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="1",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        mod_dept(
            deptId=self.reg.parent_dept_id,
            deptName=parent_name,
            parentId=100,
            orderNum=1,
            status="1",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )

    @allure.title("TC-C3: 在停用父部门下新增子部门 - 应失败")
    def test_add_child_under_disabled_parent(self):
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
                [self.reg, "parent_dept_id", f"$.data[?(@.deptName=='{self.dept_name}')].deptId"],
            ],
        )
        mod_dept(
            deptId=self.reg.parent_dept_id,
            deptName=self.dept_name,
            parentId=100,
            orderNum=1,
            status="1",
            check=[["$.msg", "eq", "操作成功"], ["$.code", "==", 200]],
        )
        child_name = f"cud_{random.randint(100, 999)}"  # 短名称，确保先触发“父部门停用”校验
        add_dept(
            deptName=child_name,
            parentId=self.reg.parent_dept_id,
            orderNum=1,
            status="0",
            check=[
                ["$.code", "!=", 200],
                ["$.msg", "include", "部门停用"],
            ],
        )
