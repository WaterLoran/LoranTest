---
name: lorantest-logic-encapsulation
description: Logic 封装技能。指导如何将 HTTP API 封装为 Python Logic 函数，涵盖框架机制、装饰器选择、参数映射、响应处理、自动清理、命名规范、目录组织等全流程工程方法论。

---

# API 封装方法

## 1. 概述与术语

| 术语          | 定义                                                         |
| ------------- | ------------------------------------------------------------ |
| **Logic**     | 用 `@Api.json` / `@Api.urlencoded` / `@Api.form_data` / `@Api.text` 装饰的 Python 函数，封装一个 HTTP API 请求 |
| **装饰器**    | `@Api.json` 等，决定请求的 Content-Type 和必须字段           |
| **register**  | `ClassDict`（属性式字典），测试脚本中用于存储过程数据        |
| **check**     | 调用侧传入的业务断言列表                                     |
| **fetch**     | 调用侧传入的响应值提取指令                                   |
| **rsp_check** | Logic 函数内定义的 API 级默认断言                            |
| **rsp_field** | Logic 函数内定义的响应字段别名映射                           |
| **req_field** | Logic 函数内定义的函数参数→请求体字段映射                    |
| **auto_fill** | 框架自动将函数参数按名称填充到请求体的机制                   |
| **restore**   | Logic 函数内定义的自动清理/回退配置                          |

### 1.1 封装工作流

```
分析 API 接口（文档 / 源码 / 抓包）
    → 选择装饰器类型
    → 编写 Logic 函数
    → 判断 common/ 下是否已有重复 Logic
    → 不存在 → 组织到 common/ 对应目录
    → 若替代旧模块 → 彻底删除旧目录（含 __pycache__）并移除入口导入
    → 更新 __init__.py 导入链
```



## 2. 框架架构（core/logic 工作原理）

### 2.1 请求生命周期

当调用一个 Logic 函数时，框架执行以下步骤：

```
Logic 函数（被 @Api.xxx 装饰）
    │
    ▼
wrapper(**kwargs)  ← 调用侧传入 check/fetch/retry/restore/context/timeout 等
    │
    ▼
abstract_api(api_type, func, wrapper, **kwargs)
    │
    ├── 1. init_step()                          → 重置步骤上下文
    ├── 2. get_retry_and_do_retry()             → 若有 retry，循环执行直到成功
    ├── 3. 从 kwargs 提取：context, fetch, check, restore, recv_file, timeout
    ├── 4. get_api_data() → 调用 func(**kwargs) → 获取 req_method, req_url, req_json 等
    ├── 5. fill_input_context_to_req_body()     → 将 context 合并到 req_json
    ├── 6. fill_input_para_to_req_body()        → req_field 映射 + auto_fill 自动填充
    ├── 7. do_real_request()                    → BaseApi().send() 发出 HTTP 请求
    ├── 8. fetch_for_restore()                  → 若有 restore，从响应提取清理数据
    ├── 9. do_service_check()                   → 执行 check 断言
    ├── 10. do_api_check()                      → 执行 rsp_check 断言
    └── 11. do_service_fetch()                  → 执行 fetch 提取值到 register
```

### 2.2 参数填充优先级

函数参数填充到请求体的处理顺序：

1. **AST 排除**：框架用 AST 分析函数体，发现在函数体内被直接引用的参数（如 f-string 中的路径参数）不会参与自动填充
2. **req_field 映射**：若定义了 `req_field`，匹配到的参数按 JSONPath 写入请求体，然后从 kwargs 移除
3. **auto_fill 自动填充**：剩余参数按名称匹配请求体字段（支持 `_` 到 `.` 的嵌套路径转换）
4. **auto_fill = False 时**：跳过步骤 3

### 2.3 __all__ 导出

`core/logic/__init__.py` 导出以下符号，Logic 文件通过 `from core.logic import *` 获得：

```python
__all__ = [
    "Api",          # 装饰器类
    "ComplexApi",   # 复合 API 类
    "allure",       # 报告装饰器
    "register",     # ClassDict（属性式字典）
    "config",       # 全局配置对象
]
```



## 3. 装饰器类型与必须字段

### 3.1 装饰器选择矩阵

| 装饰器            | Content-Type                      | 适用 HTTP 方法 | **必须**字段                          | **可选**字段                                                 |
| ----------------- | --------------------------------- | -------------- | ------------------------------------- | ------------------------------------------------------------ |
| `@Api.json`       | application/json                  | POST, PUT      | `req_method`, `req_url`, `req_json`   | `rsp_check`, `auto_fill`, `teardown`, `timeout`, `restore`, `headers`, `req_field`, `rsp_field` |
| `@Api.urlencoded` | application/x-www-form-urlencoded | GET, DELETE    | `req_method`, `req_url`, `req_params` | `req_json`, `rsp_check`, `auto_fill`, `timeout`, `restore`, `rsp_field` |
| `@Api.form_data`  | multipart/form-data               | POST           | `req_method`, `req_url`               | `req_files`, `req_data`, `rsp_check`, `timeout`, `headers`   |
| `@Api.text`       | text/plain                        | POST           | `req_method`, `req_url`               | `req_data`, `rsp_check`                                      |

**关键规则**：

- POST/PUT 请求体为 JSON → `@Api.json`，必须定义 `req_json`（可为空 `{}`）
- GET 请求 / DELETE 请求 → `@Api.urlencoded`，必须定义 `req_params`（可为空 `{}`）
- 文件上传 → `@Api.form_data`，用 `req_files` 和 `req_data`
- DELETE 请求如果带 JSON body → 也可以用 `@Api.json`

### 3.2 装饰器堆叠顺序

装饰器必须按以下顺序堆叠（从外到内）：

```python
@Api.json            # 1. API 类型装饰器（最内层，先执行）
@allure.step("描述") # 2. allure 步骤装饰器（最外层）
def func_name(...):
    ...
```

---

## 4. Logic 函数结构

### 4.1 基础模板（@Api.json — POST/PUT）

```python
from core.logic import *


@Api.json
@allure.step("添加应用")
def add_application(name="", url="", description="", parentId=None, **kwargs):
    req_method = "POST"
    req_url = "dev-api/it-systems/save"
    req_json = {
        "name": "",
        "url": "http://baidu.com",
        "description": "应用说明",
        "parentId": 0
    }
    rsp_check = {
        "code": "SUCCESS",
        "data": {
            "name": "$.name",
            "type": "IT_SYSTEM",
        },
    }
    restore = {
        "rmv_application": {
            "ids": ["$.data.id", "to_list"]
        }
    }
    return locals()
```

### 4.2 基础模板（@Api.urlencoded — GET）

```python
@Api.urlencoded
@allure.step("查看应用详情")
def lst_application_details(id="", **kwargs):
    req_method = "GET"
    req_url = f"dev-api/it-systems/nodes/{id}/details?nodeType=IT_SYSTEM"
    req_params = {}
    auto_fill = False
    return locals()
```

### 4.3 基础模板（@Api.urlencoded — DELETE / 路径参数）

```python
@Api.urlencoded
@allure.step("删除资源")
def rmv_resource(resourceId="", **kwargs):
    req_url = f"/dev-api/system/resource/{resourceId}"
    req_method = "DELETE"
    req_params = {}
    auto_fill = False
    return locals()
```

### 4.4 基础模板（@Api.json — DELETE 带 JSON body）

```python
@Api.json
@allure.step("删除应用")
def rmv_application(ids=[], **kwargs):
    req_method = "POST"
    req_url = "dev-api/it-systems/nodes/delete"
    req_json = {
        "ids": [],
        "nodeType": "IT_SYSTEM"
    }
    rsp_check = {
        "code": "SUCCESS",
        "success": True
    }
    return locals()
```

### 4.5 基础模板（@Api.form_data — 文件上传/表单请求）

```python
@Api.form_data
@allure.step("分片上传")
def chunk_upload(filename="", **kwargs):
    fie_dir = os.path.join(FILES_PATH, "upload")
    file_path = os.path.join(fie_dir, filename)
    req_method = "POST"
    req_url = "dev-api/files/chunk-upload"
    req_files = {'file': (filename, open(file_path, 'rb'))}
    req_data = {
        "id": "4dJoboXLrWQQ",
        "chunkSize": 10485760
    }
    return locals()
```

### 4.6 函数签名规则

**必须遵守**：

1. 所有 Logic 函数的**最后一个参数**必须是 `**kwargs` —— 框架通过 kwargs 传递 check/fetch/retry 等控制参数
2. 函数参数的默认值应该与 `req_json` / `req_params` 中对应字段的默认值一致（通常为 `""` 或 `None` 或 `0` 或 `[]`）
3. **必须** `return locals()` —— 框架通过返回值获取 req_url、req_method 等所有局部变量

```python
# ✅ 正确
def add_process(name="", number="", parentId=None, **kwargs):
    ...
    return locals()

# ❌ 错误 — 缺少 **kwargs
def add_process(name="", number="", parentId=None):
    ...
    return locals()

# ❌ 错误 — 缺少 return locals()
def add_process(name="", number="", parentId=None, **kwargs):
    ...
```



## 5. 参数映射机制

### 5.1 auto_fill 自动填充（默认行为）

当 `auto_fill` 未定义或为 `True` 时，框架自动将函数参数按名称匹配到 `req_json` / `req_params` 的字段中。

**匹配规则**：参数名与请求体字段名**完全一致**时自动填充。

```python
@Api.json
@allure.step("添加流程")
def add_process(name="", number="", parentId=None, **kwargs):
    req_method = "POST"
    req_url = "api/processes"
    req_json = {
        "name": "",       # ← 自动被 name 参数填充
        "number": "",     # ← 自动被 number 参数填充
        "parentId": None  # ← 自动被 parentId 参数填充
    }
    return locals()
```

调用时：`add_process(name="流程A", number="001", parentId=reg.arch_id)`
框架会自动将参数值写入 `req_json` 的对应字段。

### 5.2 req_field 显式映射

当函数参数名与请求体字段名不一致时，使用 `req_field` 显式指定映射关系：

```python
@Api.json
@allure.step("添加制度文件")
def add_institution_file(filename="", applicability="", parentId=0, **kwargs):
    req_method = "POST"
    req_url = "api/institutions/file"
    req_json = {
        "dataName": "",
        "applicableScope": {"applicableScope": ""},
        "parentId": 0,
    }
    req_field = {
        "filename": {"jsonpath": "$.dataName"},
        "applicability": {"jsonpath": "$.applicableScope.applicableScope"},
    }
    return locals()
```

**req_field 结构**：

```python
req_field = {
    "函数参数名": {
        "jsonpath": "$.请求体中的JSONPath",   # 必须
        "generator": generator_function        # 可选，数据生成器
    }
}
```

**带 generator 的 req_field**：

```python
req_field = {
    "itSystems": {
        "jsonpath": "$.data.itSystems",
        "generator": gen_it_system_list  # 自定义生成函数
    },
}
```

### 5.3 auto_fill = False（禁用自动填充）

**必须在以下场景使用 `auto_fill = False`**：

1. URL 中有路径参数（f-string 格式）
2. 函数参数名与请求体字段名有冲突
3. GET/DELETE 请求只用路径参数、不需要 query 参数

```python
@Api.urlencoded
@allure.step("查看流程架构")
def lst_process_architecture(sid="", **kwargs):
    req_method = "GET"
    req_url = f"api/processes/{sid}/info"
    req_params = {}
    auto_fill = False  # ← sid 已在 URL 中使用，不要再填充到 req_params
    return locals()
```

**关键规则**：如果 `req_url` 使用了 f-string 引用函数参数，**必须**设置 `auto_fill = False`，否则框架会尝试将该参数也填充到请求体/参数中，导致错误。

### 5.4 context 填充（调用侧）

调用侧可通过 `context` 将之前获取的完整响应数据合并到 `req_json` 中：

```python
# 先查详情获取完整数据
lst_application_details(id=reg.app_id, fetch=[reg, "app_data", "$.data"])

# 用 context 将完整数据填充到请求体，再只修改需要改的字段
mod_application_name(context=reg.app_data, newName="新名称")
```

框架会将 `context` 递归合并到 `req_json` 中（只填充 `req_json` 已有的路径）。

### 5.5 fill_loca（位置填充）

`fill_loca` 是 `req_field` 的替代方案，用于从 context 中按 JSONPath 提取数据填充到请求体：

```python
@Api.json
@allure.step("修改流程文档-通过fill_loca方式")
def mod_process_document_by_fill_loca(**kwargs):
    req_method = "POST"
    req_url = "api/processes/process-document"
    req_json = {
        "applicableScope": {"applicableScope": ""},
        "processId": "",
        "parentId": "",
    }
    fill_loca = {
        "applicableScope": "$.data.applicableScope.applicableScope",
        "applicabilityDept": "$.data.applicableScope.applicabilityDept",
        "processId": "$.processId",
        "parentId": "$.parentId",
    }
    return locals()
```

---

## 6. 响应处理

### 6.1 rsp_check（API 级默认断言）

`rsp_check` 定义在 Logic 函数内部，每次调用该 Logic 时**自动执行**的断言。它是一个嵌套字典，结构与响应体对应：

```python
rsp_check = {
    "code": "SUCCESS",            # 字面量：响应的 code 字段必须等于 "SUCCESS"
    "success": True,              # 字面量：响应的 success 字段必须等于 True
    "data": {
        "name": "$.name",         # JSONPath 引用：响应 data.name 必须等于请求体中 $.name 的值
        "type": "IT_SYSTEM",      # 字面量：响应 data.type 必须等于 "IT_SYSTEM"
    },
}
```

**规则**：

- 叶子值为字面量 → 断言响应对应字段等于该值
- 叶子值为 `$` 开头的字符串 → 从请求体中按 JSONPath 取值，断言响应字段等于该值
- **不是每个 Logic 都需要 rsp_check**，只在有稳定默认断言需求时使用

### 6.2 rsp_field（响应字段别名）

`rsp_field` 为响应字段定义别名，使调用侧可以用简短名称而非完整 JSONPath：

```python
rsp_field = {
    "dir_id": {"jsonpath": "$.data.id"},
    "template_id": {"jsonpath": "$.data.templateId"},
}
```

调用侧使用：

```python
# 不用 rsp_field 时
add_directory(fetch=[reg, "dir_id", "$.data.id"])

# 有 rsp_field 时可以简写
add_directory(fetch=[reg, "dir_id", "dir_id"])
```

---

## 7. Teardown 与 restore

### 7.1 restore 机制

`restore` 定义在 Logic 函数内部，告诉框架在测试结束后自动调用指定的清理函数：

```python
restore = {
    "rmv_application": {             # 要调用的清理函数名
        "ids": ["$.data.id", "to_list"]  # 参数值，JSONPath 从响应中提取
    }
}
```

**restore 参数值格式**：

- 字面量：`"ids": [123]` → 直接传递
- JSONPath + 转换：`"ids": ["$.data.id", "to_list"]` → 从响应提取值并转为列表

### 7.2 调用侧 restore=True

当调用侧传入 `restore=True` 时，框架自动执行 Logic 函数中定义的 `restore` 配置。如果 Logic 没有定义 `restore`，`restore=True` 无效。

```python
# Logic 定义了 restore
add_application(name="测试", restore=True)  # 测试结束后自动删除

# Logic 未定义 restore 时
add_institution_directory(name="目录", restore=True)  # 若 Logic 内有 restore 定义才生效
```

---

## 8. 函数命名规范

### 8.1 CRUD 前缀（严格约束）

| 操作类型       | 前缀   | 示例                                                         |
| -------------- | ------ | ------------------------------------------------------------ |
| 创建/添加      | `add_` | `add_process`, `add_institution_file`, `add_organization`    |
| 修改/更新      | `mod_` | `mod_architecture_name`, `mod_diagram_of_process`, `mod_institution_link_with_data` |
| 查询/列表/详情 | `lst_` | `lst_process`, `lst_institution_nodes`, `lst_application_details` |
| 删除           | `rmv_` | `rmv_process`, `rmv_institution_directory`, `rmv_application` |

### 8.2 其他操作前缀

| 操作类型  | 前缀        | 示例                                                         |
| --------- | ----------- | ------------------------------------------------------------ |
| 设置/配置 | `set_`      | `set_architecture_card`, `set_institution_file_attributes_with_data` |
| 发布      | `publish_`  | `publish_processes_node_norecord`, `publish_institution_file` |
| 提交      | `submit_`   | `submit_institution_file`, `submit_process_file`             |
| 下载      | `download_` | `download_process_file`, `download_institution_file`         |
| 移动      | `mov_`      | `mov_application`, `mov_process`, `mov_institution_file`     |
| 排序      | `sort_`     | `sort_application`, `sort_institution`, `sort_processes`     |
| 搜索      | `search_`   | `search_process`, `search_file_nodes`, `search_risk`         |
| 复制      | `copy_`     | `copy_processes`, `copy_processes_include_child_nodes`       |
| 转换      | `convert_`  | `convert_process_file_to_process`, `convert_institution_file_to_process` |
| 批量操作  | `batch_`    | `batch_lock_architecture_node`                               |
| 还原      | `revert_`   | `revert_process_in_recycle_bin`, `revert_file_in_recycle_bin` |
| 生成      | `generate_` | `generate_architecture_diagram`, `generate_organization_diagram` |

### 8.3 命名约定

- **使用 `lst_` 而非 `get_`** 用于查询操作
- 带 `_completely` 后缀表示彻底删除（含子节点回收站等）：`rmv_process_architecture_completely`
- 带 `_norecord` 后缀表示不记录文控的发布：`publish_processes_node_norecord`
- 带 `_with_data` 后缀表示使用完整数据对象：`set_institution_file_attributes_with_data`

### 8.4 allure.step 描述

```python
@allure.step("添加应用")           # 中文简述操作
@allure.step("查看流程架构")        # 中文简述操作
@allure.step("查看制度配置==>即后台管理->制度管理->制度配置")  # 复杂路径可用 ==> 和 -> 描述
```



## 9. Logic 文件组织

### 9.1 单个logic文件内的组织

一个完整的 Logic 文件应该包含一个模块的所有相关 API 封装：

```python
# user_management_logic.py
"""
用户管理模块 API 封装
封装完成后的 Logic 文件
"""

# 注意：由于框架设计，使用 from core.logic import *
from core.logic import *
import allure

# 1. 用户增删改查
@Api.json
@allure.step("添加用户-add_user")
def add_user(...):
    ...

@Api.urlencoded  
@allure.step("查看用户列表-lst_user")
def lst_user(...):
    ...

# 2. 用户状态管理
@Api.json
@allure.step("启用用户-enable_user")
def enable_user(...):
    ...

# 3. 用户权限管理
@Api.json
@allure.step("分配角色-assign_role")
def assign_role(...):
    ...
```

### 9.2 统一位置

**所有Logic文件必须放在 `common/` 目录下**

- ✅ 正确：`common/system_management_logic/post_management_logic/basic.py`
- ❌ 错误：`position_task/api_encapsulation/post_management_logic.py`

### 9.3 按URL路径组织

**严格按照API的URL路径来组织目录结构**

```
URL路径: /dev-api/system/post
对应目录: common/system_management_logic/post_management_logic/
```

### 9.4 分层导入结构

```
common/
├── ruoyi_logic.py                    # 总入口
├── system_management_logic/          # 系统管理模块
│   ├── __init__.py                   # 导入子模块
│   └── post_management_logic/        # 岗位管理
│       ├── __init__.py               # 只导入，不定义函数
│       └── basic.py                  # 实际Logic文件
```

### 9.5 文件大小控制

- 单个文件：100-200行，包含4-6个API
- 超过7个API → 创建目录拆分到多个文件
- `__init__.py` 只用于导入，不定义API函数

### 9.6 清理旧模块（替代/迁移时）

当用新的 Logic 模块替代或迁移旧模块时，必须**彻底删除旧目录**，避免残留导致混淆或误导入：

- 删除旧目录下的**所有内容**：包括 `.py` 文件、`__pycache__` 目录及其中的 `.pyc` 文件等
- 删除**目录本身**：如 `common/department_management_logic` 整目录移除（如使用 `rm -rf common/xxx`）
- 同步修改入口：从 `common/ruoyi_logic.py`（或其它总入口）中移除对旧模块的 `from common.xxx import *`

### 9.7  完整工作流示例

```python
# 1. 分析API URL
# POST /dev-api/system/post

# 2. 创建目录结构
# common/system_management_logic/post_management_logic/

# 3. 编写Logic文件 (basic.py)
from core.logic import *
@api(method="POST", path="/system/post")
def add_position(positionName: str = None):
    req_json = {"postName": positionName}
    return locals()

# 4. 更新导入链
# post_management_logic/__init__.py: from .basic import *
# system_management_logic/__init__.py: 添加 from .post_management_logic import *

# 5. 创建测试目录结构
# cases/ruoyi/api/system_management/post_management/

# 6. 编写测试脚本
from common.ruoyi_logic import *
result = add_position(positionName="测试岗位")
```


