# 字典管理模块 - 疑似 BUG 记录

> 以下 BUG 均通过测试脚本执行日志分析发现，结合请求体、响应体进行判定。
> 分析日志批次：20260307_231xxx（最新执行）

---

## BUG-1: 查询不存在的字典类型返回 msg=null 【待确认】

- **关联用例**: DC-T11 (`test_dict_type_detail_not_exist`)
- **复现步骤**: GET `/system/dict/type/999999`（不存在的 dictId）
- **实际结果**: 返回 `{"msg": null, "code": 500}`
- **预期结果**: 应返回明确的错误提示信息，如 `"字典类型不存在"` 或 `"数据不存在"`
- **影响**: msg=null 导致前端无法展示友好错误提示，用户无法理解操作失败原因
- **严重级别**: 中
- **BUG 类型**: 错误处理
- **确认证据**: 日志 `test_dict_validation_20260307_231300.log`：响应 `{"msg": null, "code": 500}`

---

## BUG-2: 查询不存在的字典数据返回 msg=null 【待确认】

- **关联用例**: DC-D08 (`test_dict_data_detail_not_exist`)
- **复现步骤**: GET `/system/dict/data/999999`（不存在的 dictCode）
- **实际结果**: 返回 `{"msg": null, "code": 500}`
- **预期结果**: 应返回明确的错误提示信息，如 `"字典数据不存在"`
- **影响**: 同 BUG-1，用户无法获得有意义的错误反馈
- **严重级别**: 中
- **BUG 类型**: 错误处理
- **确认证据**: 日志 `test_dict_validation_20260307_231300.log`：响应 `{"msg": null, "code": 500}`

---

## BUG-3: 修改不存在的字典类型返回 msg=null 【待确认】

- **关联用例**: DC-T27 (`test_dict_type_modify_not_exist`)
- **复现步骤**: PUT `/system/dict/type`，body 中 dictId=999999（不存在的类型）
- **实际结果**: 返回 `{"msg": null, "code": 500}`
- **预期结果**: 应返回明确的错误提示信息，如 `"字典类型不存在，无法修改"`
- **影响**: 同 BUG-1，错误提示不友好
- **严重级别**: 中
- **BUG 类型**: 错误处理
- **确认证据**: 日志 `test_dict_validation_20260307_231300.log`：响应 `{"msg": null, "code": 500}`

---

## BUG-4: 删除有子数据的字典类型时错误提示含义模糊 【待确认】

- **关联用例**: DC-T32 (`test_dict_type_delete_with_data`)
- **复现步骤**:
  1. 创建字典类型
  2. 在该类型下创建字典数据
  3. 尝试删除该字典类型
- **实际结果**: 返回 `"val_type_xxx已分配,不能删除"`
- **预期结果**: 提示应更清晰明确，如 `"该字典类型下存在字典数据，不能删除"`
- **影响**: "已分配"措辞容易让用户困惑，不清楚是被什么分配、该如何处理
- **严重级别**: 低
- **BUG 类型**: 用户体验
- **确认证据**: 日志 `test_dict_validation_20260307_231300.log`：删除响应 `"val_type_xxx已分配,不能删除"`

---

## BUG-5: pageNum=0 未校验，等效于 pageNum=1 【待确认】

- **关联用例**: DC-N01 (`test_dict_type_list_page_zero`)
- **复现步骤**: GET `/system/dict/type/list?pageNum=0&pageSize=10`
- **实际结果**: 返回 200，正常返回第一页数据（total=25, rows=10条），行为等同于 pageNum=1
- **预期结果**: 应拒绝非法 pageNum（返回错误码），或明确文档说明 pageNum=0 被规范化为 1
- **影响**: pageNum=0 是无意义的页码，静默处理可能掩盖前端 bug（如页码从0开始的错误）
- **严重级别**: 低
- **BUG 类型**: 输入校验
- **确认证据**: 日志 `test_dict_edge_cases_20260307_231258.log`：请求 pageNum=0 → 响应 200，返回正常分页数据
