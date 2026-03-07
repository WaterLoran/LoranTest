---
name: lorantest-scripting
description: 在用户要求编写 LoranTest 测试脚本时触发。指导如何编写 pytest 测试脚本，涵盖类结构、register 用法、Logic 调用参数（check/fetch/retry/restore/context）、数据清理、断言体系、复杂场景编排等完整工程方法论。Logic 封装规则见 logic_encapsulation skill。

---

# LoranTest 测试脚本编写完整指南

## 1. 核心概念

| 概念         | 说明                                                       |
| ------------ | ---------------------------------------------------------- |
| **Logic**    | 封装了 HTTP API 的 Python 函数，放在 `common/` 目录下      |
| **测试脚本** | 放在 `cases/` 目录下，组合调用 Logic 函数完成测试场景      |
| **register** | `ClassDict`（属性式字典），存储测试过程中产生的 ID、数据等 |
| **check**    | 调用 Logic 时传入的业务层响应断言                          |
| **fetch**    | 调用 Logic 时传入的响应值提取指令                          |
| **retry**    | 调用 Logic 时传入的重试次数                                |
| **restore**  | 调用 Logic 时传入的自动清理标记                            |
| **context**  | 调用 Logic 时传入的上下文数据，合并到请求体中              |

### 1.1 关键约束

- **Logic 文件**中使用 `from core.logic import *`
- **测试脚本**中使用 `from common.epros_logic import *`
- **禁止**在测试脚本中使用 `from core.logic import *`（会导致 `NameError: Api`）

---

## 2. 测试脚本基本结构

### 2.1 标准模板

```python
# coding: utf-8
from common.ruoyi_logic import *


class TestFeatureName001(object):
    def setup_method(self):
        pass

    @allure.title("测试标题-中文描述")
    def test_feature_name_001(self):
        # Precondition operation:
        # [1]按照测试目的自行构造

        # Procedure:
        # [1]正向操作

        # Expected results:
        # [1]操作成功

        reg = register({
            "resource_id": None,
        })
        self.reg = reg

        # 测试步骤...

    def teardown_method(self):
        # 数据清理...
        pass
```

### 2.2 导入声明

```python
# coding: utf-8
from common.ruoyi_logic import *
```

这一行导入了：

- 所有 Logic 函数（`add_process`, `lst_institution_nodes`, ...）
- 框架工具（`register`, `config`, `allure`, `edit_json_data`, `timestamp_str`, ...）
- 断言工具（`check_excel`, `check_time`, `check_obj`）
- 文件操作（`write_register`, `read_register`）

**按需追加导入**（仅在特定场景需要）：

```python
import time          # time.sleep() 等待异步操作
import pytest        # pytest.skip() 等
from pages import *  # UI 自动化测试时
from core.mysql import *  # 数据库操作时
```

---

## 3. 类结构与命名

### 3.1 类命名规范

格式：`Test{功能描述}{编号}`

```python
class TestNewProcessFile001(object):           # 功能 + 编号
class TestDuplicateNameVerification001(object): # 场景描述 + 编号
class TestBugPatch517202404001(object):         # Bug修复 + 日期 + 编号
class TestAddProcessArchitecture001(object):    # 操作 + 对象 + 编号
class TestSubmitInstitution001(object):         # 操作 + 对象 + 编号
```

**规则**：

- 必须以 `Test` 开头（pytest 发现机制）
- 继承 `object` 或不写（API 测试）；继承 `EprosUicase`（UI 测试）
- 编号用三位数字 `001`, `002`, ...

### 3.2 测试方法命名

格式：`test_{功能描述}_{编号}`

```python
def test_new_process_file_001(self):
def test_duplicate_name_verification_001(self):
def test_bug_patch517_202404_001(self):
def test_information_statistics_detail_download_001(self):
```

### 3.3 测试步骤注释模板

```python
@allure.title("测试标题")
def test_xxx_001(self):
    # Precondition operation:
    # [1]系统运行正常

    # Procedure:
    # [1]创建架构
    # [2]在架构下创建流程
    # [3]发布流程

    # Expected results:
    # [1]成功
    # [2]成功
    # [3]成功

    # [1]创建架构
    # [1]成功
    add_process_architecture(...)

    # [2]在架构下创建流程
    # [2]成功
    add_process(...)
```

---

## 4. register() 用法

### 4.1 创建 register

`register()` 创建一个 `ClassDict`（支持属性访问的字典），用于存储测试过程中产生的数据：

```python
reg = register({
    "architecture_id": None,
    "process_id": None,
    "diagram_id": None,
    "card_data": None,
    "one_activity_node": {},
})
self.reg = reg  # 挂到 self 上以便 teardown 使用
```

### 4.2 属性访问

```python
reg.architecture_id       # 读取
reg.architecture_id = 123 # 写入
reg["architecture_id"]    # 也可以用字典方式
```

### 4.3 fetch 写入 register

`fetch` 会将响应中的值写入 register：

```python
add_process_architecture(
    name="架构A",
    fetch=[reg, "architecture_id", "id"]  # 将响应中 $.id 的值写入 reg.architecture_id
)
# 之后可直接使用 reg.architecture_id
```

### 4.4 rebuild_dict()

当使用 `edit_json_data` 修改了 register 中的嵌套数据后，必须调用 `rebuild_dict()` 将内部的 `ClassDict` 转回普通 dict：

```python
edit_json_data(json_data=reg.one_activity_node, update={...})
reg.rebuild_dict()  # 必须调用，否则嵌套数据的类型可能不正确
```

### 4.5 跨脚本持久化

```python
write_register(__file__, reg)  # 将 register 写入本地 JSON 文件
read_register(__file__, reg)   # 从本地 JSON 文件恢复 register
```

---

## 5. Logic 调用参数详解

### 5.1 check（业务层断言）

**格式**：`[JSONPath, 比较符, 期望值]` 或包含多个断言的二维列表

```python
# 单个断言
add_process(name="流程A", check=["$..data..name", "eq", "流程A"])

# 多个断言
lst_process_architecture(
    sid=reg.id1,
    check=[
        ["$..sourceNode.id", "eq", reg.id1],
        ["name", "eq", "架构名称"]
    ]
)

# exist 断言（判断 JSONPath 是否匹配到数据）
lst_latest_released_architecture(
    check=[f"$.data[?(@.link.name=='{var_name}')]", "exist", True]
)

# 错误码断言（预期失败场景）
add_process(
    name="重复名称", parentId=reg.parent_id,
    check=[
        ["$.code", "eq", "A0422"],
        ["$.data..message", "eq", "已存在名称为[重复名称]的节点"],
    ]
)
```

**禁用 check**：

```python
download_file(recordId=reg.id, check=False)  # 文件下载等无标准 JSON 响应的场景
```

### 5.2 check 支持的比较符

| 符号          | 别名                         | 含义                                            |
| ------------- | ---------------------------- | ----------------------------------------------- |
| `eq`          | `==`, `equal`                | 相等                                            |
| `!=`          | `not_equal`, `not_eq`        | 不等                                            |
| `>`           | `lg`, `larger`, `greater`    | 大于                                            |
| `<`           | `smaller`, `less`            | 小于                                            |
| `>=`          | `greater_equal`              | 大于等于                                        |
| `<=`          | `less_equal`                 | 小于等于                                        |
| `in`          | —                            | 值在目标集合中                                  |
| `not_in`      | —                            | 值不在目标集合中                                |
| `include`     | —                            | 目标包含在响应值中（子串/子集）                 |
| `not_include` | —                            | 目标不包含在响应值中                            |
| `exist`       | —                            | JSONPath 是否匹配到数据（target 为 True/False） |
| `len>`        | `length_greater`, `len_lg`   | 长度大于                                        |
| `len<`        | `length_smaller`, `len_less` | 长度小于                                        |
| `len==`       | `length_equal`, `len_eq`     | 长度等于                                        |

**不支持** `contains`，用 `include` 代替。

### 5.3 fetch（响应值提取）

**格式**：`[register对象, "键名", "JSONPath表达式"]`

```python
# 单个 fetch（两种写法等价）
add_process(fetch=[reg, "process_id", "id"])
add_process(fetch=[reg, "process_id", "$.data.id"])

# 多个 fetch（使用二维列表）
add_process(
    fetch=[
        [reg, "process_id", "id"],
        [reg, "supportFileDirId", "$.data.supportFileDirId"],
    ]
)

# fetch 完整对象
lst_process(sid=reg.process_id, fetch=[reg, "diagram_id", "$.data.id"])

# fetch 带 JSONPath 过滤的数据
lst_process(
    sid=reg.process_id,
    fetch=[[reg, "one_activity_node", "$.data.nodes[?(@.zIndex==5)]"]]
)

# fetch 到 register 后使用
lst_application_details(id=reg.app_id, fetch=[reg, "app_data", "$.data"])
mod_application_name(context=reg.app_data, newName="新名字")
```

### 5.4 retry（重试）

用于异步操作（发布、下载、统计等），框架会重复调用直到 check 通过或达到最大次数：

```python
# 等待发布结果
lst_latest_released_architecture(
    check=[f"$.data[?(@.link.name=='{var_name}')]", "exist", True],
    retry=60  # 最多重试 60 次
)

# 等待下载任务完成
lst_download_detailed_report(
    recordId=reg.recordId,
    check=["$..status", "eq", "SUCCESSFUL"],
    retry=60
)
```

**使用场景**：发布后查询、异步任务状态轮询、ES 索引更新等。

### 5.5 restore（自动清理）

调用侧传入 `restore=True`，框架在测试结束后自动执行 Logic 中定义的清理操作：

```python
add_process_architecture(
    name="架构A",
    fetch=[reg, "architecture_id", "id"],
    restore=True  # 测试结束后自动删除该架构
)

add_application(
    name="应用A",
    fetch=[reg, "app_id", "$.data.id"],
    restore=True  # 测试结束后自动删除该应用
)
```

**注意**：`restore=True` 依赖 Logic 函数内部定义了 `restore` 配置。如果 Logic 没有定义 `restore`，传 `restore=True` 无效。

### 5.6 context（上下文填充）

将之前查询到的完整数据对象作为请求体的基础：

```python
# 1. 先查询详情获取完整数据
lst_application_details(id=reg.app_id, fetch=[reg, "app_data", "$.data"])

# 2. 用 context 传入完整数据，只修改需要改的字段
mod_application_name(
    context=reg.app_data,
    newName="新名字前缀_" + var_app_name
)
```

**原理**：框架将 `context` 递归合并到 `req_json` 中，然后再用其他显式参数覆盖特定字段。

### 5.7 timeout（超时设置）

```python
publish_processes_architecture(
    nodeId=reg.architecture_id,
    number="A1111",
    description="描述",
    timeout=60  # 秒
)
```

### 5.8 recv_file（接收文件）

```python
download_detailed_report(
    recordId=reg.recordId,
    recv_file="report_download.xls",  # 保存到 files/ 目录
    check=False
)
```

---

## 6. 数据生成

### 6.1 命名策略

**核心原则**：测试数据名称必须包含测试方法名，便于定位数据来源。

```python
var_architecture = "架构_test_new_process_file_001"
var_process = "流程_test_new_process_file_001"
var_institution = "制度目录test_submit_institution_001"
var_app_name = "应用_test_use_context_001"
```

### 6.2 时间戳与随机值

```python
timestamp_str()                        # 字符串时间戳，如 "1709827200"
timestamp_int()                        # 整数时间戳
generate_random_string(12)             # 12 位随机字符串
generate_12_random_string(reg, "key")  # 生成 12 位随机串并写入 reg
```

### 6.3 文件名

```python
filename = "EPROSV5.0-功能验证列表（售后).docx"  # 直接使用 files/ 目录下的文件
filename = "new_institution_file_001.txt"          # 简单文件名
```

---

## 7. 数据清理规则（关键）

### 7.1 清理策略选择

| 策略           | 适用场景                            | 实现方式                                      |
| -------------- | ----------------------------------- | --------------------------------------------- |
| `restore=True` | Logic 定义了 restore 配置           | 调用时传入 `restore=True`，teardown 中 `pass` |
| 手动 teardown  | Logic 未定义 restore 或需要精确控制 | teardown_method 中手动调用 `rmv_*`            |
| 混合策略       | 部分数据用 restore，部分手动清理    | 结合使用                                      |

### 7.2 使用 restore=True 的模式

```python
class TestFeature001(object):
    def setup_method(self):
        pass

    def test_feature_001(self):
        reg = register({"id1": None})
        self.reg = reg

        add_institution_directory(
            name="目录A", parentId=0,
            fetch=[reg, "id1", "$.data.id"],
            restore=True  # 自动清理
        )
        add_institution_file(filename="file.txt", parentId=reg.id1)

    def teardown_method(self):
        pass  # restore=True 会自动清理
```

### 7.3 手动 teardown 的模式

```python
def teardown_method(self):
    rmv_process_architecture_completely(
        ids=[self.reg.architecture_id]
    )
```

### 7.4 层级数据从下往上删除

父子关系的数据**必须先删子再删父**：

```python
def teardown_method(self):
    # 先删流程
    rmv_process_completely(ids=[self.reg.process_id])
    # 再删架构
    rmv_process_architecture_completely(ids=[self.reg.architecture_id])
```

### 7.5 审批数据清理

对于已提交审批的数据，必须先完成审批流程才能删除：

```python
def teardown_method(self):
    lst_user_all_task(fetch=[reg, "task_id", "$.data[0].id"])
    approval_task_all_passed(task_id=reg.task_id)
    rmv_process_architecture_completely(ids=[self.reg.architecture_id])
```

### 7.6 配置恢复

修改了系统配置的测试，必须在 teardown 中恢复：

```python
def teardown_method(self):
    set_process_same_directory_verification()  # 恢复为默认配置
    rmv_process_architecture_completely(ids=[self.reg.architecture_id])
```

### 7.7 预期失败的操作不需要清理

如果操作预期会失败（如重复名称校验），不会产生数据，不需要 fetch 和清理：

```python
add_process(
    name="重复名称", parentId=reg.parent_id,
    check=[["$.code", "eq", "A0422"]]  # 预期失败，无需 fetch
)
```

---

## 8. setup_method 模式

### 8.1 简单测试（无前置条件）

```python
def setup_method(self):
    pass
```

### 8.2 复杂前置条件

```python
def setup_method(self):
    reg = register({
        "architecture_id": None,
        "process_id": None,
        "diagram_id": None,
        "one_activity_node": {},
    })
    self.reg = reg

    # 开启必要配置
    set_overview_statistics_of_view_role_of_system_admin(restore=True)

    # 创建基础数据
    var_architecture = "架构_test_name_001"
    add_process_architecture(
        name=var_architecture,
        fetch=[[reg, "architecture_id", "id"]],
        restore=True
    )

    var_process = "流程_test_name_001"
    add_process(
        name=var_process, parentId=reg.architecture_id,
        fetch=[[reg, "process_id", "id"], [reg, "supportFileDirId", "$.data.supportFileDirId"]]
    )
```

### 8.3 setup 中还是 test 中初始化 register

| 模式                  | 适用场景                             |
| --------------------- | ------------------------------------ |
| setup_method 中初始化 | 前置条件复杂，需要提前构建大量数据   |
| test 方法中初始化     | 简单测试，前置条件与测试步骤紧密相关 |

---

## 9. 响应验证体系

### 9.1 JSONPath 基础

```python
# 简单路径
"$.code"                                    # 响应体的 code 字段
"$.data.id"                                 # 嵌套路径
"$.data.sourceNode.isPublished"             # 深层嵌套

# 递归查找
"$..data..name"                             # 递归查找 data 下的 name
"$..sourceNode.id"                          # 递归查找 sourceNode 下的 id

# 过滤表达式
"$.data[?(@.name=='架构A')]"                # 按条件过滤
"$.data[?(@.link.name=='流程A')]"           # 嵌套对象过滤
"$.data.nodes[?(@.type=='activity')]"       # 按类型过滤
"$.data.nodes[?(@.zIndex==5)]"             # 按数值过滤

# 索引访问
"$.data[0].id"                              # 第一个元素
"$.[0].name"                                # 根数组第一个元素
```

### 9.2 JSONPath 中特殊字符处理

`@`、`#`、`'` 等字符会破坏 JSONPath filter 表达式。处理方式：

```python
# 方案 1：用 API 参数过滤后取索引
lst_institution_nodes(name=special_name, fetch=[reg, "id", "$.data[0].id"])

# 方案 2：使用 f-string 构造（当名称不含特殊字符时）
check=[f"$.data[?(@.name=='{var_name}')]", "exist", True]
```

### 9.3 exist 断言

验证某个 JSONPath 是否匹配到数据：

```python
lst_latest_released_architecture(
    check=[f"$.data[?(@.link.name=='{var_architecture}')]", "exist", True],
    retry=60
)
```

### 9.4 负向断言

测试预期失败的场景，**必须用具体的错误信息断言**：

```python
# ✅ 推荐 — 精确验证错误码和错误信息
add_process(
    name="重复名称", parentId=reg.parent_id,
    check=[
        ["$.code", "eq", "A0422"],
        ["$.data..message", "eq", "已存在名称为[重复名称]的节点"],
    ]
)

# ❌ 不推荐 — 无法区分是哪种错误
add_process(name="重复名称", check=[["$.code", "!=", 200]])
```

### 9.5 Excel 断言

```python
check_excel({
    "file": "report.xls",                    # files/ 目录下的文件名
    "sheet": "活动信息化详情报表",              # sheet 名称（默认 Sheet1）
    "condition": [                            # 过滤条件
        {"column_name": "系统名称", "column_value": "应用A"},
        {"column_name": "所属流程", "column_value": "流程B"},
    ],
    "assert_type": "equal",                   # 断言类型
    "target": 1                               # 期望匹配行数
})
```

**condition 简写格式**：

```python
"condition": [
    ["人员名称", "张三"],        # [列名, 列值]
    ["人员账号", 88880001],
]
```

**assert_type 选项**：

| 类型    | 含义             |
| ------- | ---------------- |
| `equal` | 等于             |
| `<=`    | 左边是右边的子集 |
| `=>`    | 右边是左边的子集 |

**target 格式**：

- 整数：期望匹配行数，如 `1`, `2`
- 列表：期望匹配行的列值断言：

```python
"target": [
    {"column_name": "功能角色", "column_value": "销售工程师"},
    {"column_name": "年龄", "column_value": 25},
]
```

### 9.6 时间断言

```python
check_time(
    exp_timestamp=reg.some_time,
    check_type="==",         # ==, earlier, later
    target_timestamp=reg.other_time
)
```

### 9.7 对象断言

```python
check_obj(obj=some_list, attr="length", assert_type="eq", target=5)
```

---

## 10. 复杂场景编排

### 10.1 多步骤流程测试

```python
@allure.title("发布流程")
def test_process_publish_001(self):
    reg = register({
        "architecture_id": None,
        "process_id": None,
        "template_id": None,
        "card_data": None,
    })
    self.reg = reg

    # 步骤 1: 创建架构
    add_process_architecture(
        name="架构A", number="A", nameEn="A", code="A",
        fetch=[[reg, "architecture_id", "id"]],
    )

    # 步骤 2: 创建流程
    add_process(
        name="流程A", parentId=reg.architecture_id,
        fetch=[[reg, "process_id", "id"]],
    )

    # 步骤 3: 设置审批模板
    set_architecture_task(
        relatedId=reg.architecture_id,
        templateId=config.approve_template.process.four_reviewer_release_by_drafter.id
    )

    # 步骤 4: 设置架构卡片
    lst_architecture_card(processId=reg.architecture_id, fetch=[reg, "card_data", "$.data.data"])
    edit_json_data(json_data=reg.card_data, update={"description": "流程描述"})
    set_architecture_card(data=reg.card_data, processId=reg.architecture_id)

    # 步骤 5: 发布
    publish_processes_architecture(
        nodeId=reg.architecture_id, number="V1", description="首次发布", timeout=60
    )

    # 步骤 6: 验证发布状态
    lst_process(sid=reg.process_id, check=["$.data.sourceNode.isPublished", "eq", True])
```

### 10.2 数据依赖链

fetch 的结果可以作为后续步骤的输入：

```python
# 创建架构 → 获取 ID → 在架构下创建流程 → 获取画布 ID → 修改画布
add_process_architecture(name="架构", fetch=[reg, "arch_id", "id"])
add_process(name="流程", parentId=reg.arch_id, fetch=[reg, "process_id", "id"])
lst_process(sid=reg.process_id, fetch=[reg, "diagram_id", "$.data.id"])
add_default_diagram_for_process_2_role_2_activity(diagramId=reg.diagram_id)
```

### 10.3 edit_json_data 修改复杂数据

从响应中 fetch 出复杂 JSON 对象，修改后作为参数传回：

```python
# 1. 获取活动节点数据
lst_process(
    sid=reg.process_id,
    fetch=[[reg, "one_activity_node", "$.data.nodes[?(@.zIndex==5)]"]]
)

# 2. 修改节点数据
edit_json_data(
    json_data=reg.one_activity_node,
    update={
        "data": {
            "executionRole": {
                "roleId": "2XfVV5q3IPik",
                "roleText": "角色"
            },
            "itSystems": [
                {
                    "itSystem": reg.it_system_node,
                    "launchTime": "",
                    "transactionCode": "",
                    "url": ""
                }
            ],
        },
    }
)

# 3. 必须 rebuild_dict
reg.rebuild_dict()

# 4. 将修改后的数据保存
mod_diagram_of_process(
    version=1,
    diagramId=reg.diagram_id,
    node=reg.one_activity_node,
)
```

### 10.4 异步操作等待

对于发布、下载等异步操作，使用 `retry` 轮询直到完成：

```python
# 提交下载任务
submit_download_detailed_report(
    itSystemIds=[reg.app_id],
    fetch=[reg, "recordId", "$.recordId"]
)

# 轮询等待下载完成
lst_download_detailed_report(
    recordId=reg.recordId,
    check=["$..status", "eq", "SUCCESSFUL"],
    retry=60
)

# 下载文件
download_detailed_report(
    recordId=reg.recordId,
    recv_file="report.xls",
    check=False
)
```

必要时也可以用 `time.sleep()` 等待：

```python
mod_diagram_of_process(...)
time.sleep(3)  # 等待画布数据同步
lst_process(...)
```

### 10.5 config 全局配置使用

```python
# 使用预配置的审批模板 ID
config.approve_template.architecture.four_reviewer_release_by_drafter.id
config.approve_template.process.four_reviewer_release_by_drafter.id
config.approve_template.institution.four_reviewer_release_by_drafter.id

# 使用预配置的用户信息
config.user.designer_1.id
```

---

## 11. Allure 报告装饰器

```python
@allure.feature("流程体系")    # 功能模块（可选）
@allure.story("架构管理")      # 用户故事（可选）
class TestXxx(object):

    @allure.title("新建流程架构")  # 测试标题（推荐必填）
    def test_xxx_001(self):
        ...
```

**实践规则**：

- `@allure.title()` 使用中文简述测试目的，**每个测试方法都应有**
- `@allure.feature()` / `@allure.story()` 按需使用

---

## 12. 文件位置与目录结构

```
cases/
├── design_end/               # 设计端测试
│   ├── process/              # 流程相关
│   │   ├── architecture/     # 架构操作
│   │   │   └── new/
│   │   │       └── test_add_process_architecture_001.py
│   │   └── ...
│   ├── batch_file_upload/    # 批量上传
│   ├── convert_to_process/   # 转换为流程
│   └── lock_function_new/    # 锁定功能
├── browser_end/              # 浏览端测试
├── regression/               # 回归测试
│   ├── smoke/                # 冒烟测试（核心路径）
│   │   ├── process_system/
│   │   └── institution/
│   ├── general/              # 通用回归
│   │   ├── back_stage_management/
│   │   └── browser_end/
│   └── bug/                  # Bug 修复验证
│       ├── 202404/
│       └── 202405/
├── precondition/             # 前置条件脚本
├── project/                  # 项目级脚本（准备/清理数据）
├── example/                  # 示例脚本
└── unfiled_script/           # 未归类脚本
```

**组织原则**：

- 按业务端（design_end / browser_end / regression）分顶层目录
- regression 下按测试类型分（smoke / general / bug）
- 具体目录按业务模块层级组织

---

## 13. 常见陷阱速查

| 现象                                            | 原因                                    | 修复                                                |
| ----------------------------------------------- | --------------------------------------- | --------------------------------------------------- |
| `NameError: Api`                                | 测试脚本用了 `from core.logic import *` | 改为 `from common.epros_logic import *`             |
| `TypeError: 'bool' object is not subscriptable` | fetch 的 JSONPath 匹配不到数据          | 检查响应结构；检查名称是否含特殊字符                |
| `contains` 比较符报错                           | 不支持该比较符                          | 用 `include` 代替                                   |
| teardown 删除报错"存在下级"                     | 删除顺序错误                            | 先删子再删父                                        |
| `RuntimeError: No active exception to reraise`  | check 的 JSONPath 在响应中不存在        | 确认响应结构，用 `exist` 而非 `eq None`             |
| 测试后数据残留                                  | 未清理或 restore 未生效                 | 检查 restore 配置或添加手动 teardown                |
| fetch 值为 None                                 | JSONPath 表达式错误或响应结构变化       | 打印响应确认结构，修正 JSONPath                     |
| `reg.rebuild_dict()` 遗漏                       | `edit_json_data` 后未重建               | 在 `edit_json_data` 后立即调用 `reg.rebuild_dict()` |
| retry 超时                                      | 异步操作耗时超出重试次数                | 增大 retry 值或检查操作是否有异常                   |
| config 属性找不到                               | 配置文件中未定义                        | 检查 `config/` 目录下的配置文件                     |

---

## 14. 编写测试脚本检查清单

编写每个测试脚本时，逐项检查：

- [ ] 文件头 `# coding: utf-8` 和 `from common.epros_logic import *`
- [ ] 类名以 `Test` 开头，方法名以 `test_` 开头
- [ ] 有 `setup_method` 和 `teardown_method`
- [ ] register 中声明了所有需要存储的 ID/数据
- [ ] register 挂到了 `self.reg`（teardown 需要使用时）
- [ ] 每个创建操作都有对应的 fetch（获取 ID）或 restore=True
- [ ] teardown 中正确清理了所有测试数据
- [ ] 层级数据从下往上删除
- [ ] 使用了 `@allure.title()` 描述测试目的
- [ ] 测试数据名称包含测试方法名（便于追溯）
- [ ] 预期失败的场景使用了精确的错误信息断言
- [ ] 异步操作使用了 retry 或 time.sleep
- [ ] `edit_json_data` 后调用了 `reg.rebuild_dict()`