---
name: logic封装技能
description: 使用python对API进行封装, 输出一段python代码, 可用于pytest脚本编写

---

# API 封装方法

## 1.0 术语

logic: 对API封装之后的代码, 即为logic



## 1.1 封装API的概念与工作流

**封装API**是指将 HTTP API 请求封装成 Python 函数的过程。这个过程包括：

1. 分析 API 文档或接口或源代码
2. 创建 Python 函数包装 API 调用
3. 配置请求参数、路径、方法等
4. 定义响应处理逻辑
5. 判断当前封装得到的logic在common目录下是否已经有重复的logic了
6. 如果在common目录下没有重复的logic则将logic文件组织到common目录下

**封装完成后得到的代码文件称为 Logic**（逻辑文件），这是封装工作的最终产出物。

**工作流**：

```
分析API → 封装API → 得到Logic → 判断logic是否已存在 → 不存在则组织到common的对应目录下
```



## 1.2 logic基本结构

```python
# 注意：由于框架设计，Logic文件中使用 from core.logic import *
# 而不是 from core.logic import Api，以避免循环导入问题
from core.logic import *
import allure

@Api.json  # 或 @Api.urlencoded, @Api.form_data
@allure.step("API描述-英文名称")
def api_function(param1="", param2="", **kwargs):
    """
    函数说明
    """
    req_url = "/dev-api/system/endpoint"  # API路径
    req_method = "POST"  # 或 GET, PUT, DELETE
    req_json = {  # 对于 @Api.json
        "field1": "",    # 字段默认值
        "field2": 0,
    }
    # 或 req_params = {}  # 对于 @Api.urlencoded
    # 或 req_data = {}  # 对于 @Api.form_data
    # 或 req_files = {}  # 对于 @Api.form_data
    
    req_field = {  # 请求字段映射
        "param1": {"jsonpath": "$.field1"},
        "param2": {"jsonpath": "$.field2"},
    }
    
    rsp_field = {  # 响应字段提取
        "msg": {"jsonpath": "$.msg"},
        "data": {"jsonpath": "$.data"},
    }
    
    rsp_check = {  # API级别的响应检查
        "msg": "操作成功",
        "code": 200,
    }
    
    return locals()  # 必须返回 locals()
```

## 1.3 Logic 文件组织

### 1.3.1 单个logic文件内的组织

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

### 1.3.1 统一位置

**所有Logic文件必须放在 `common/` 目录下**

- ✅ 正确：`common/system_management_logic/post_management_logic/basic.py`
- ❌ 错误：`position_task/api_encapsulation/post_management_logic.py`

### 1.3.2 按URL路径组织

**严格按照API的URL路径来组织目录结构**

```
URL路径: /dev-api/system/post
对应目录: common/system_management_logic/post_management_logic/
```

### 1.3.3 分层导入结构

```
common/
├── ruoyi_logic.py                    # 总入口
├── system_management_logic/          # 系统管理模块
│   ├── __init__.py                   # 导入子模块
│   └── post_management_logic/        # 岗位管理
│       ├── __init__.py               # 只导入，不定义函数
│       └── basic.py                  # 实际Logic文件
```

### 1.3.4 文件大小控制

- 单个文件：100-200行，包含4-6个API
- 超过7个API → 创建目录拆分到多个文件
- `__init__.py` 只用于导入，不定义API函数

### 1.3.5 完整工作流示例

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



## 1.4 不同请求类型的处理

### 1.4.1 json类型请求

支持的请求方法: POST, PUT

必须字段: `req_url`, `req_method`, `req_json`（可为空 dict）

```python
from core.logic import Api
import allure

@Api.json
@allure.step("添加资源-add_resource")
def add_resource(name="", code="", **kwargs):
    req_url = "/dev-api/system/resource"
    req_method = "POST"
    req_json = {
        "resourceName": "",
        "resourceCode": "",
        "status": "0",
    }
    req_field = {
        "name": {"jsonpath": "$.resourceName"},
        "code": {"jsonpath": "$.resourceCode"},
    }
    return locals()
```



### 1.4.2 urlencoded类型请求

支持的请求方法: GET, DELETE

是否支持路径参数: 可以支持

必须字段: `req_url`, `req_method`, `req_params`

非必须字段: auto_fill, req_json

```python
from core.logic import Api
import allure

@Api.urlencoded  # GET请求用urlencoded
@allure.step("查看资源详情-get_resource")
def get_resource(resourceId="", **kwargs):
    req_url = f"/dev-api/system/resource/{resourceId}"
    req_method = "GET"
    req_params = {}  # 必须定义，即使是空字典
    auto_fill = False  # 重要：路径参数需要这个设置
    return locals()

@Api.json  # DELETE请求用json
@allure.step("删除资源-rmv_resource")
def rmv_resource(resourceId="", **kwargs):
    req_url = f"/dev-api/system/resource/{resourceId}"
    req_method = "DELETE"
    req_json = {}  # 不一定需要定义
    auto_fill = False  # 重要：路径参数需要这个设置
    return locals()

@Api.urlencoded
@allure.step("查看资源列表-lst_resource")
def lst_resource(name="", code="", pageNum=1, pageSize=10, **kwargs):
    req_url = "/dev-api/system/resource/list"
    req_method = "GET"
    req_params = {
        "resourceName": "",
        "resourceCode": "",
        "pageNum": 1,
        "pageSize": 10,
    }
    return locals()
```

### 1.4.3 form_data类型请求



```python
from core.logic import Api
import allure

@Api.form_data
@allure.step("分片上传")
def chunk_upload(filename=""):
    fie_dir = os.path.join(FILES_PATH, "upload")
    logger.debug(f"分片上传函数中::文件所在目录为{fie_dir}, filename为{filename}")
    file_path = os.path.join(fie_dir, filename)
    create_file_from_backup(file_path)  # 检查目标文件是否存在，若不存在则从备用文件复制创建
    req_method = "POST"
    req_url = "csvc-file/files/chunk-upload"
    req_files = {'file': (filename, open(file_path, 'rb'))}
    req_data = {
        "id": "4dJoboXLrWQQ",  # TODO 这里需要保持和chunk_merge关键字的一致
        "chunkSize": 10485760  # 表示文件的分片大小为10M, 即如果不超过10M, 则直接当成一个分片去上传
    }
    return locals()
```



### 1.4.4 命名规范

- **Logic 文件**：`模块名_logic.py`（如 `user_management_logic.py`, `post_management_logic.py`）
- **API 函数**：`操作_资源()`（如 `add_user()`, `lst_user()`, `mod_position()`, `rmv_post()`）

**严格约束**：

- **添加数据**：必须以 `add_` 开头（如 `add_position`, `add_user`）
- **修改数据**：必须以 `mod_` 开头（如 `mod_position`, `mod_user`）
- **查询数据**：必须以 `lst_` 开头（如 `lst_position`, `lst_user`, `lst_position_detail`）
- **删除数据**：必须以 `rmv_` 开头（如 `rmv_position`, `rmv_user`）
- **其他类型**：只有非CRUD操作才允许不使用上述四种前缀（如 `export_position`, `optionselect_position`）

**重要经验**：查询操作应使用 `lst_` 前缀，而不是 `get_`。例如，查询岗位详情应命名为 `lst_position_detail`，而不是 `get_position`。



## 1.5 关键参数说明

| 参数         | 说明                          | 必需 |
| ------------ | ----------------------------- | ---- |
| `req_url`    | API路径，支持f-string格式     | ✅    |
| `req_method` | HTTP方法                      | ✅    |
| `req_json`   | JSON请求体（@Api.json时）     | ✅    |
| `req_params` | 查询参数（@Api.urlencoded时） | ✅    |
| `auto_fill`  | 路径参数时为False             | 可选 |
| `req_field`  | 参数到请求字段的映射          | 可选 |
| `rsp_field`  | 响应字段提取                  | 可选 |
| `rsp_check`  | API级别响应检查               | 可选 |