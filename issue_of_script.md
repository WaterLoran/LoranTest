# 脚本质量审查问题记录

> 审查时间：2026-03-07
> 审查标准：ISS-1~ISS-7（详见 lorantest-judge-bug SKILL）

---

## 岗位管理模块（test_post_management）

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_basic_crud.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: TC-A11 `test_delete_single_post` 和 TC-A19 `test_detail_after_delete` 使用 `check=[["$.code", "in", [200, 500]]]` 骑墙断言，未明确删除后查详情的业务预期
- **建议修改**: 删除后查详情应期望 `$.code == 500` 或 `$.data == null`，明确"已删除不可查"的预期
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_basic_crud.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-A14 `test_export_no_filter` 和 TC-A15 `test_export_with_filter` 使用 `export_position(check=[])` 无任何断言
- **建议修改**: 至少校验 HTTP 状态码或响应头 Content-Type
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_edge_cases.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: TC-K02 `test_detail_nonexistent` 使用 `check=[["$.code", "in", [200, 500]]]`，未明确查询不存在岗位的预期
- **建议修改**: 应明确期望 `code == 500`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_edge_cases.py

- **问题类型**: ISS-4 空测试方法
- **具体描述**: TC-K07 `test_invalid_json` 方法体为空仅设 `self.reg.position_id = None`；TC-K08 `test_list_invalid_page_num` 和 TC-K09 `test_list_invalid_page_size` 标题为"非法"但实际传入合法值
- **建议修改**: 补充实际非法输入测试逻辑（如 `pageNum=-1`, `pageSize="abc"`），或标记为 `@pytest.mark.skip("待实现")`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_uniqueness.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: TC-G11 `test_name_case_sensitive` 使用 `check=[["$.code", "in", [200, 500]]]`，未明确名称大小写唯一性的业务预期
- **建议修改**: 根据业务规则明确期望：若区分大小写则 `eq 200`，若不区分则 `eq 500`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_code_validation.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-C03~C10（7个用例）创建后仅校验 `$.code == 200`，未通过详情接口验证存储的 `postCode` 值
- **建议修改**: 增加 `lst_position_detail` + `check=[["$.data.postCode", "eq", code]]`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_code_validation.py

- **问题类型**: ISS-6 数据命名不规范
- **具体描述**: TC-C03 `test_code_one_char` 使用 `random.choice(["x","y","z","a","b"])` 单字符编码无 case_id 前缀，易冲突难追溯
- **建议修改**: 改为带前缀的唯一编码如 `f"TC_C03_{random_char}_{timestamp}"`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_name_validation.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-B03, B06~B08, B11~B13（共7个用例）创建后仅校验 `$.code == 200`，未验证存储的 `postName` 值
- **建议修改**: 增加详情查询 + 对 `$.data.postName` 的断言
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_name_validation.py

- **问题类型**: ISS-6 数据命名不规范
- **具体描述**: TC-B03 `test_name_one_char` 使用 `one_char_names = ["岗","测","A","Z","1","9"]` 随机取单字符无 case_id 前缀
- **建议修改**: 改为带前缀的名称或确保唯一性
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_delete_constraints.py

- **问题类型**: ISS-7 前置数据依赖存量
- **具体描述**: TC-H02 和 TC-H04 创建用户时硬编码 `deptId=100, roleIds=[2]`，依赖系统存量数据
- **建议修改**: 在 setup 中动态创建专用部门和角色，或至少在注释中说明依赖条件
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_sort_validation.py

- **问题类型**: ISS-3 数据清理缺失
- **具体描述**: TC-D10 `test_same_sort_multiple` 使用局部 `reg = register(...)` 而非 `self.reg`，fetch 的 position_id 不在 teardown 清理路径上
- **建议修改**: 改为使用 `self.reg` 或在 teardown 中添加对局部变量 ID 的清理
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_data_integrity.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-L06 `test_export_and_list_consistent` 使用 `export_position(..., check=[])` 无断言，标题说"导出与列表一致"但未实际校验
- **建议修改**: 校验导出文件内容或至少验证响应状态
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_post_management/test_post_status_validation.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-E05 `test_status_non_numeric` 仅校验 `$.code == 500`，未校验错误提示信息内容
- **建议修改**: 增加 `["$.msg", "include", "状态"]` 或类似的 msg 断言
- **发现时间**: 2026-03-07
---

## 部门管理模块（test_dept_management）

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_basic_crud.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-A1 创建部门后未通过详情接口验证存储的字段值（如 deptName, orderNum, status 等）
- **建议修改**: 增加详情查询 + 对 `$.data.deptName` 等字段的断言
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_boundary.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-O3 最小数据创建部门后未验证存储数据
- **建议修改**: 增加详情查询验证存储值
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_field_validation.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-J1/J6/J10/J13 边界值创建后未验证存储值；特别是 TC-J13（带空格名称）未检查存储的 deptName 是否已 trim
- **建议修改**: 增加详情查询断言，尤其是 TC-J13 应验证 `$.data.deptName` 是否为 trim 后的值
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_field_validation.py

- **问题类型**: ISS-6 数据命名不规范
- **具体描述**: TC-J2 使用 `"a"*31` 无可追溯前缀，数据残留时难以定位来源
- **建议修改**: 改为带 case_id 前缀的命名如 `f"TC_J2_{'a'*25}"`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_hierarchy_advanced.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-G7 将父节点设为子孙节点后仅断言 `code==200`，未明确拒绝预期（实际应拒绝循环引用）
- **建议修改**: 应断言 `code==500`，明确"不允许将父部门设为其子孙部门"的业务预期
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_order_sort.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-M5 标题为验证排序对列表的影响，但未实际断言列表顺序
- **建议修改**: 查询列表后对返回数据的顺序做断言
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_status_transitions.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-H6 停用部门后未验证 status 实际变更
- **建议修改**: 查询详情断言 `$.data.status == "1"`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_delete_scenarios.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-L6 重复删除断言 `code==200` 未质疑预期（重复删除应返回错误）
- **建议修改**: 应断言 `code==500`，期望"部门不存在"或类似错误
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_validation.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: TC-E2 特殊字符部门创建后未验证存储的名称
- **建议修改**: 查询详情断言名称与请求一致
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_validation.py

- **问题类型**: ISS-7 前置数据依赖存量
- **具体描述**: TC-E1 硬编码 `999999` 作为不存在的 deptId，依赖假设该 ID 不存在
- **建议修改**: 改为动态获取不存在的 ID 或使用更可靠的方式
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dept_management/test_dept_validation.py

- **问题类型**: ISS-6 数据命名不规范
- **具体描述**: TC-D2 使用 `"a"*40` 无 case_id 标识
- **建议修改**: 改为带前缀命名
- **发现时间**: 2026-03-07
---

## 字典管理模块（test_dict_management）

### cases/test_ruoyi/test_api/test_system_management/test_dict_management/test_dict_edge_cases.py

- **问题类型**: ISS-3 数据清理缺失（严重脚本BUG）
- **具体描述**: 多处将 `self._own_dict_type`（变量）写成了 `"self._own_dict_type"`（字符串字面量），导致数据创建在错误的类型名下，teardown 清理的是正确变量值对应的类型，字面量类型下的数据不会被清理。影响 6 个测试方法
- **建议修改**: 将所有 `"self._own_dict_type"` 字符串改为 `self._own_dict_type` 变量引用
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dict_management/test_dict_validation.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: `test_dict_type_detail_not_exist`（DC-T11）和 `test_dict_data_detail_not_exist`（DC-D08）使用 `check=[["$.code", "in", [200, 404, 500]]]`，同时接受成功和失败
- **建议修改**: 根据业务规则明确期望（通常应为 500 或 404）
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dict_management/test_dict_edge_cases.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: DC-N01、DC-N07、DC-C02、DC-D31 等多个测试仅断言 `$.code == 200`，未对返回数据做业务层面校验
- **建议修改**: 增加对返回数据结构和关键字段的断言
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dict_management/test_dict_validation.py

- **问题类型**: ISS-3 数据清理缺失
- **具体描述**: `test_dict_type_modify_duplicate_type`（DC-T28）创建两个字典类型，teardown 仅清理一个 ID，若中途失败另一个类型会残留
- **建议修改**: 在 register 中注册两个 ID，teardown 中逐个清理
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dict_management/test_dict_data_basic_crud.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: DC-D03、DC-D10、DC-N03 等仅断言响应码，未验证筛选条件/排序是否真正生效
- **建议修改**: 增加对返回数据的条件验证
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_dict_management/test_dict_type_basic_crud.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: DC-T35 删除后查 optionselect 未验证目标不在列表中；DC-T30 修改后未验证新名称出现在结果中
- **建议修改**: 增加对列表内容的断言
- **发现时间**: 2026-03-07
---

## 角色管理模块（test_role_management）

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_admin_protection.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: K05 `test_rmv_role_not_exist`、L03~L06 共5个用例使用 `$.code in [200, 500]` 骑墙断言
- **建议修改**: 根据业务规则明确各操作的预期返回码
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_admin_protection.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: K08 `test_rmv_then_list_invisible` 标题为"删除后列表不可见"，仅断言删除的 code=200，未查询列表验证
- **建议修改**: 增加列表查询 + 验证已删除角色不在列表中
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_admin_protection.py

- **问题类型**: ISS-3 数据清理缺失
- **具体描述**: L03 `test_add_role_remark_over_500` 若系统返回200，角色被创建但未 fetch role_id，teardown 无法清理
- **建议修改**: 增加 fetch 提取 role_id，teardown 中清理
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_name_validation.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: B02 `test_add_role_name_over_30` 使用 `$.code in [200, 500]`，日志确认系统返回500明确拒绝
- **建议修改**: 改为 `eq 500`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_key_validation.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: C02 `test_add_role_key_over_100` 使用 `$.code in [200, 500]`，日志确认系统返回500明确拒绝
- **建议修改**: 改为 `eq 500`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_sort_validation.py

- **问题类型**: ISS-1 模糊断言
- **具体描述**: D04 `test_add_role_sort_negative` 和 D06 `test_add_role_sort_decimal` 使用 `$.code in [200, 500]` 骑墙断言，掩盖了系统接受非法值的问题
- **建议修改**: 改为 `eq 500`（期望拒绝负数/小数）
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_sort_validation.py

- **问题类型**: ISS-3 数据清理缺失
- **具体描述**: D04/D06 系统均返回200（日志确认），角色已创建但未 fetch role_id 导致数据残留
- **建议修改**: 增加 fetch 提取 role_id，确保 teardown 清理
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_role_management/test_role_management_lifecycle_001.py

- **问题类型**: ISS-5 缺少 allure 标注
- **具体描述**: 类缺少 `@allure.feature` / `@allure.story`，方法缺少 `@allure.title`
- **建议修改**: 为每个 test 方法添加 `@allure.title("简短中文描述")`
- **发现时间**: 2026-03-07
---

## 用户管理模块（test_user_management）

### cases/test_ruoyi/test_api/test_system_management/test_user_management/test_add_user_998.py

- **问题类型**: ISS-5 缺少 allure 标注
- **具体描述**: `test_add_user_998` 方法缺少 `@allure.title()` 装饰器
- **建议修改**: 添加 `@allure.title("添加用户基本功能验证")`
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_user_management/test_adit_person_picture.py

- **问题类型**: ISS-2 仅校验响应码
- **具体描述**: `test_person_picture_01` 仅调用 `mod_profile_picture()` 无任何自定义断言，依赖API层默认断言
- **建议修改**: 增加查询个人资料接口验证头像 URL 已更新
- **发现时间**: 2026-03-07
---

### cases/test_ruoyi/test_api/test_system_management/test_user_management/test_adit_person_picture.py

- **问题类型**: ISS-5 缺少 allure 标注
- **具体描述**: `test_person_picture_01` 方法缺少 `@allure.title()` 装饰器
- **建议修改**: 添加 `@allure.title("修改个人头像")`
- **发现时间**: 2026-03-07
---

## 汇总统计

| 模块 | ISS-1 | ISS-2 | ISS-3 | ISS-4 | ISS-5 | ISS-6 | ISS-7 | 合计 |
|------|-------|-------|-------|-------|-------|-------|-------|------|
| 岗位管理 | 4 | 5 | 1 | 3 | 0 | 2 | 1 | 16 |
| 部门管理 | 0 | 8 | 0 | 0 | 0 | 2 | 1 | 11 |
| 字典管理 | 1 | 4 | 2 | 0 | 0 | 0 | 0 | 7 |
| 角色管理 | 7 | 1 | 2 | 0 | 1 | 0 | 0 | 11 |
| 用户管理 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 3 |
| **合计** | **12** | **19** | **5** | **3** | **3** | **4** | **2** | **48** |
