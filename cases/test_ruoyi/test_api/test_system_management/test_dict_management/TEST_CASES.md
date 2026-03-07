# 字典管理测试用例（≥100 条）

## 一、字典类型 - 列表与查询

### DC-T01 字典类型-无筛选分页列表
- **前置条件**：已登录，具备 system:dict:list 权限。
- **步骤**：
  1. GET /system/dict/type/list，params: pageNum=1, pageSize=10。
- **预期结果**：
  1. HTTP 200，code=200；返回 rows 数组、total 数字；total≥0。
- **依赖接口**：GET /system/dict/type/list。

### DC-T02 字典类型-按字典名称模糊查询
- **前置条件**：已登录，存在部分字典类型数据。
- **步骤**：
  1. GET /system/dict/type/list，params: dictName=某关键字（如“用户”）。
- **预期结果**：
  1. code=200，rows 中仅包含 dictName 含该关键字的记录。
- **依赖接口**：GET /system/dict/type/list。

### DC-T03 字典类型-按字典类型精确查询
- **前置条件**：已登录，已知某 dictType（如 sys_user_sex）。
- **步骤**：
  1. GET /system/dict/type/list，params: dictType=sys_user_sex。
- **预期结果**：
  1. code=200，rows 中仅一条且 dictType 等于该值。
- **依赖接口**：GET /system/dict/type/list。

### DC-T04 字典类型-按状态正常筛选
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/type/list，params: status=0。
- **预期结果**：
  1. code=200，rows 中每条 status 均为 0。
- **依赖接口**：GET /system/dict/type/list。

### DC-T05 字典类型-按状态停用筛选
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/type/list，params: status=1。
- **预期结果**：
  1. code=200，rows 中每条 status 均为 1。
- **依赖接口**：GET /system/dict/type/list。

### DC-T06 字典类型-分页 pageSize 为 1
- **前置条件**：已登录，至少有一条类型数据。
- **步骤**：
  1. GET /system/dict/type/list，params: pageNum=1, pageSize=1。
- **预期结果**：
  1. code=200，rows 长度为 1，total≥1。
- **依赖接口**：GET /system/dict/type/list。

### DC-T07 字典类型-查询无匹配时空列表
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/type/list，params: dictType=non_existent_type_xyz。
- **预期结果**：
  1. code=200，rows 为空数组，total=0。
- **依赖接口**：GET /system/dict/type/list。

### DC-T08 字典类型-多条件组合查询
- **前置条件**：已登录，存在满足条件的类型。
- **步骤**：
  1. GET /system/dict/type/list，params: dictName=某值, dictType=某值, status=0, pageNum=1, pageSize=10。
- **预期结果**：
  1. code=200，返回满足所有条件的记录。
- **依赖接口**：GET /system/dict/type/list。

### DC-T09 字典类型-列表响应结构完整性
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/type/list，params: pageNum=1, pageSize=10。
- **预期结果**：
  1. 响应包含 code、msg、rows、total；rows 中元素含 dictId、dictName、dictType、status 等。
- **依赖接口**：GET /system/dict/type/list。

### DC-T10 字典类型-查询详情
- **前置条件**：已登录，已知有效 dictId。
- **步骤**：
  1. GET /system/dict/type/{dictId}。
- **预期结果**：
  1. code=200，data 含该类型的 dictId、dictName、dictType、status、remark 等。
- **依赖接口**：GET /system/dict/type/{dictId}。

### DC-T11 字典类型-详情不存在的 dictId
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/type/999999（假定不存在）。
- **预期结果**：
  1. 返回 404 或 code 非 200，或 msg 提示不存在。
- **依赖接口**：GET /system/dict/type/{dictId}。

---

## 二、字典类型 - 新增

### DC-T12 字典类型-新增仅必填
- **前置条件**：已登录，具备 system:dict:add。
- **步骤**：
  1. POST /system/dict/type，body: dictName=测试类型A, dictType=test_type_a（符合 ^[a-z][a-z0-9_]*$）。
- **预期结果**：
  1. code=200，msg 为“操作成功”或等价；可据此在列表中查到新记录。
- **依赖接口**：POST /system/dict/type。

### DC-T13 字典类型-新增全字段
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=全字段类型, dictType=test_full, status=0, remark=备注内容。
- **预期结果**：
  1. code=200，新增成功；列表/详情中可见上述字段。
- **依赖接口**：POST /system/dict/type。

### DC-T14 字典类型-新增 status=1
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=停用类型, dictType=test_disabled, status=1。
- **预期结果**：
  1. code=200，新增成功；详情中 status=1。
- **依赖接口**：POST /system/dict/type。

### DC-T15 字典类型-新增 dictName 为空失败
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=, dictType=test_empty_name。
- **预期结果**：
  1. 返回 400/500 或 code 非 200，提示“字典名称不能为空”或等价。
- **依赖接口**：POST /system/dict/type。

### DC-T16 字典类型-新增 dictType 为空失败
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=名称, dictType=。
- **预期结果**：
  1. 返回参数校验错误，提示“字典类型不能为空”或等价。
- **依赖接口**：POST /system/dict/type。

### DC-T17 字典类型-新增 dictType 格式错误（大写）
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=测试, dictType=TestType。
- **预期结果**：
  1. 返回格式校验错误，提示“字典类型必须以字母开头…”或等价。
- **依赖接口**：POST /system/dict/type。

### DC-T18 字典类型-新增 dictType 含特殊字符失败
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=测试, dictType=test-type。
- **预期结果**：
  1. 返回格式校验错误（仅允许小写字母、数字、下划线）。
- **依赖接口**：POST /system/dict/type。

### DC-T19 字典类型-重复 dictType 新增失败
- **前置条件**：已存在 dictType=sys_user_sex（或先新增一条）。
- **步骤**：
  1. POST /system/dict/type，body: dictName=另一名称, dictType=sys_user_sex。
- **预期结果**：
  1. 返回业务错误，提示“字典类型已存在”或等价。
- **依赖接口**：POST /system/dict/type。

### DC-T20 字典类型-新增后列表可见
- **前置条件**：已登录，使用唯一 dictType。
- **步骤**：
  1. POST /system/dict/type 新增一条；
  2. GET /system/dict/type/list 按 dictType 查询。
- **预期结果**：
  1. 新增成功；
  2. 列表中能查到该条且字段一致。
- **依赖接口**：POST /system/dict/type，GET /system/dict/type/list。

### DC-T21 字典类型-dictType 恰 100 字符
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，dictType 为 100 个符合规则的字符。
- **预期结果**：
  1. 新增成功（若系统允许）或返回长度限制错误。
- **依赖接口**：POST /system/dict/type。

### DC-T22 字典类型-dictName 超 100 字符失败
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，dictName 为 101 字符。
- **预期结果**：
  1. 返回长度校验错误。
- **依赖接口**：POST /system/dict/type。

---

## 三、字典类型 - 修改

### DC-T23 字典类型-正常修改
- **前置条件**：已存在一条类型（dictId 已知）。
- **步骤**：
  1. PUT /system/dict/type，body: dictId, dictName=新名称, dictType=原type或新type（唯一）, status=0, remark=新备注。
- **预期结果**：
  1. code=200，修改成功；详情/列表中为新值。
- **依赖接口**：PUT /system/dict/type。

### DC-T24 字典类型-仅修改 dictName
- **前置条件**：已存在一条类型。
- **步骤**：
  1. PUT /system/dict/type，body: dictId, dictName=仅改名称, 其余不变。
- **预期结果**：
  1. code=200，仅 dictName 变更。
- **依赖接口**：PUT /system/dict/type。

### DC-T25 字典类型-仅修改 status
- **前置条件**：已存在类型 status=0。
- **步骤**：
  1. PUT /system/dict/type，body: dictId, status=1，其余不变。
- **预期结果**：
  1. code=200，status 变为 1。
- **依赖接口**：PUT /system/dict/type。

### DC-T26 字典类型-修改 dictType 后数据表同步
- **前置条件**：已存在类型 A 及其下若干字典数据。
- **步骤**：
  1. PUT /system/dict/type 将类型 A 的 dictType 改为 B；
  2. GET /system/dict/data/type/B 查询数据。
- **预期结果**：
  1. 修改成功；
  2. 原属于 A 的数据现以 dictType=B 返回。
- **依赖接口**：PUT /system/dict/type，GET /system/dict/data/type/{dictType}。

### DC-T27 字典类型-修改不存在的 dictId
- **前置条件**：已登录。
- **步骤**：
  1. PUT /system/dict/type，body: dictId=999999, dictName=x, dictType=test_x。
- **预期结果**：
  1. 返回错误（404 或业务提示）。
- **依赖接口**：PUT /system/dict/type。

### DC-T28 字典类型-修改后唯一性冲突
- **前置条件**：已存在类型 dictType=type_a 和 type_b。
- **步骤**：
  1. PUT /system/dict/type，将 type_b 的 dictType 改为 type_a。
- **预期结果**：
  1. 返回“字典类型已存在”或等价错误。
- **依赖接口**：PUT /system/dict/type。

### DC-T29 字典类型-仅修改 remark
- **前置条件**：已存在一条类型。
- **步骤**：
  1. PUT /system/dict/type，body: dictId, remark=新备注，其余不变。
- **预期结果**：
  1. code=200，仅 remark 变更。
- **依赖接口**：PUT /system/dict/type。

### DC-T30 字典类型-修改后 optionselect 包含新值
- **前置条件**：已存在类型，修改其 dictName。
- **步骤**：
  1. PUT /system/dict/type 修改 dictName；
  2. GET /system/dict/type/optionselect。
- **预期结果**：
  1. 修改成功；
  2. optionselect 列表中该条 dictName 为新值。
- **依赖接口**：PUT /system/dict/type，GET /system/dict/type/optionselect。

---

## 四、字典类型 - 删除

### DC-T31 字典类型-无数据时删除成功
- **前置条件**：已存在一条类型且其下无字典数据。
- **步骤**：
  1. DELETE /system/dict/type/{dictId}。
- **预期结果**：
  1. code=200，删除成功；列表/详情不再包含该条。
- **依赖接口**：DELETE /system/dict/type/{dictIds}。

### DC-T32 字典类型-有数据时禁止删除
- **前置条件**：已存在类型且其下至少一条字典数据。
- **步骤**：
  1. DELETE /system/dict/type/{dictId}。
- **预期结果**：
  1. 返回业务错误，提示“已分配,不能删除”或等价。
- **依赖接口**：DELETE /system/dict/type/{dictIds}。

### DC-T33 字典类型-批量删除
- **前置条件**：已存在多条无数据的类型，dictId 为 id1, id2, id3。
- **步骤**：
  1. DELETE /system/dict/type/id1,id2,id3。
- **预期结果**：
  1. code=200，三条均删除；列表中均不可见。
- **依赖接口**：DELETE /system/dict/type/{dictIds}。

### DC-T34 字典类型-删除后列表不包含
- **前置条件**：已存在类型，记 dictId。
- **步骤**：
  1. DELETE /system/dict/type/{dictId}；
  2. GET /system/dict/type/list 查询。
- **预期结果**：
  1. 删除成功；
  2. rows 中无该 dictId。
- **依赖接口**：DELETE，GET list。

### DC-T35 字典类型-删除后 optionselect 不包含
- **前置条件**：已存在类型。
- **步骤**：
  1. DELETE /system/dict/type/{dictId}；
  2. GET /system/dict/type/optionselect。
- **预期结果**：
  1. 删除成功；
  2. optionselect 列表中无该类型。
- **依赖接口**：DELETE，optionselect。

### DC-T36 字典类型-删除不存在的 dictId
- **前置条件**：已登录。
- **步骤**：
  1. DELETE /system/dict/type/999999。
- **预期结果**：
  1. 返回 404 或业务错误（视实现而定）。
- **依赖接口**：DELETE /system/dict/type/{dictIds}。

---

## 五、字典类型 - 导出与 optionselect

### DC-T37 字典类型-导出 Excel
- **前置条件**：已登录，具备 system:dict:export。
- **步骤**：
  1. POST /system/dict/type/export，params 同列表（可选）。
- **预期结果**：
  1. HTTP 200，响应为 Excel 文件流或 Content-Type 为 Excel。
- **依赖接口**：POST /system/dict/type/export。

### DC-T38 字典类型-optionselect 全量
- **前置条件**：已登录（可选，该接口可能无需权限）。
- **步骤**：
  1. GET /system/dict/type/optionselect。
- **预期结果**：
  1. code=200，返回类型列表数组，元素含 dictId、dictName、dictType 等。
- **依赖接口**：GET /system/dict/type/optionselect。

### DC-T39 字典类型-导出带条件
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type/export，params: dictType=某值。
- **预期结果**：
  1. 导出的数据与列表使用相同条件时一致（仅格式为 Excel）。
- **依赖接口**：POST /system/dict/type/export。

---

## 六、字典数据 - 列表与查询

### DC-D01 字典数据-列表按 dictType
- **前置条件**：已登录，存在某类型的字典数据。
- **步骤**：
  1. GET /system/dict/data/list，params: dictType=sys_user_sex, pageNum=1, pageSize=10。
- **预期结果**：
  1. code=200，rows 中每条 dictType 均为该值。
- **依赖接口**：GET /system/dict/data/list。

### DC-D02 字典数据-列表按 dictLabel 模糊
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/data/list，params: dictLabel=男。
- **预期结果**：
  1. code=200，rows 中 dictLabel 包含“男”。
- **依赖接口**：GET /system/dict/data/list。

### DC-D03 字典数据-列表按 status
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/data/list，params: status=0。
- **预期结果**：
  1. code=200，rows 中每条 status=0。
- **依赖接口**：GET /system/dict/data/list。

### DC-D04 字典数据-分页
- **前置条件**：已登录，某类型下有多条数据。
- **步骤**：
  1. GET /system/dict/data/list，params: dictType=某类型, pageNum=1, pageSize=2。
- **预期结果**：
  1. code=200，rows 长度≤2，total≥0。
- **依赖接口**：GET /system/dict/data/list。

### DC-D05 字典数据-无匹配空列表
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/data/list，params: dictType=non_exist_type_xyz。
- **预期结果**：
  1. code=200，rows 为空，total=0。
- **依赖接口**：GET /system/dict/data/list。

### DC-D06 字典数据-按类型查数据 type 接口
- **前置条件**：已登录，某类型下有正常状态数据。
- **步骤**：
  1. GET /system/dict/data/type/{dictType}。
- **预期结果**：
  1. code=200，返回该类型下数据列表（通常仅 status=0，按 dictSort 排序）。
- **依赖接口**：GET /system/dict/data/type/{dictType}。

### DC-D07 字典数据-详情
- **前置条件**：已存在字典数据，dictCode 已知。
- **步骤**：
  1. GET /system/dict/data/{dictCode}。
- **预期结果**：
  1. code=200，data 含 dictCode、dictLabel、dictValue、dictType、dictSort、status 等。
- **依赖接口**：GET /system/dict/data/{dictCode}。

### DC-D08 字典数据-详情不存在的 dictCode
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/data/999999。
- **预期结果**：
  1. 返回 404 或业务错误。
- **依赖接口**：GET /system/dict/data/{dictCode}。

### DC-D09 字典数据-列表响应结构
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/data/list，params: pageNum=1, pageSize=10。
- **预期结果**：
  1. 响应含 code、rows、total；rows 元素含 dictCode、dictLabel、dictValue、dictType、dictSort、status。
- **依赖接口**：GET /system/dict/data/list。

### DC-D10 字典数据-多条件组合
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/data/list，params: dictType=某类型, dictLabel=某值, status=0。
- **预期结果**：
  1. code=200，返回同时满足条件的记录。
- **依赖接口**：GET /system/dict/data/list。

---

## 七、字典数据 - 新增

### DC-D11 字典数据-新增仅必填
- **前置条件**：已存在类型 dictType=test_type；已登录。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=标签1, dictValue=value1, dictType=test_type。
- **预期结果**：
  1. code=200，新增成功；列表可查到且 dictLabel/dictValue/dictType 正确。
- **依赖接口**：POST /system/dict/data。

### DC-D12 字典数据-新增全字段
- **前置条件**：已存在类型；已登录。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel, dictValue, dictType, dictSort=1, cssClass=, listClass=default, isDefault=N, status=0, remark=备注。
- **预期结果**：
  1. code=200，各字段保存正确。
- **依赖接口**：POST /system/dict/data。

### DC-D13 字典数据-dictLabel 为空失败
- **前置条件**：已登录，已存在类型。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=, dictValue=v, dictType=某类型。
- **预期结果**：
  1. 返回校验错误，“字典标签不能为空”或等价。
- **依赖接口**：POST /system/dict/data。

### DC-D14 字典数据-dictValue 为空失败
- **前置条件**：已登录，已存在类型。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=l, dictValue=, dictType=某类型。
- **预期结果**：
  1. 返回校验错误，“字典键值不能为空”或等价。
- **依赖接口**：POST /system/dict/data。

### DC-D15 字典数据-dictType 为空失败
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=l, dictValue=v, dictType=。
- **预期结果**：
  1. 返回校验错误。
- **依赖接口**：POST /system/dict/data。

### DC-D16 字典数据-新增 isDefault=Y
- **前置条件**：已存在类型；已登录。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=默认, dictValue=Y, dictType=某类型, isDefault=Y。
- **预期结果**：
  1. code=200，详情中 isDefault=Y。
- **依赖接口**：POST /system/dict/data。

### DC-D17 字典数据-新增 dictSort
- **前置条件**：已存在类型；已登录。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=x, dictValue=x, dictType=某类型, dictSort=99。
- **预期结果**：
  1. code=200，列表/详情中 dictSort=99；/type/{dictType} 顺序符合 dictSort。
- **依赖接口**：POST /system/dict/data。

### DC-D18 字典数据-新增后 type 接口可见
- **前置条件**：已存在类型 test_type；已登录。
- **步骤**：
  1. POST /system/dict/data 新增一条 dictType=test_type；
  2. GET /system/dict/data/type/test_type。
- **预期结果**：
  1. 新增成功；
  2. 返回列表中包含新数据（含缓存时也一致）。
- **依赖接口**：POST /system/dict/data，GET /system/dict/data/type/{dictType}。

### DC-D19 字典数据-新增后列表可见
- **前置条件**：已存在类型；已登录。
- **步骤**：
  1. POST /system/dict/data 新增；
  2. GET /system/dict/data/list 按 dictType/dictLabel 查。
- **预期结果**：
  1. 新增成功；
  2. 列表中能查到该条。
- **依赖接口**：POST，GET list。

### DC-D20 字典数据-新增 cssClass listClass
- **前置条件**：已存在类型；已登录。
- **步骤**：
  1. POST /system/dict/data，body: dictLabel=l, dictValue=v, dictType=某类型, cssClass=primary, listClass=default。
- **预期结果**：
  1. code=200，详情中 cssClass、listClass 正确。
- **依赖接口**：POST /system/dict/data。

---

## 八、字典数据 - 修改与删除

### DC-D21 字典数据-正常修改
- **前置条件**：已存在字典数据，dictCode 已知。
- **步骤**：
  1. PUT /system/dict/data，body: dictCode, dictLabel=新标签, dictValue=新值, dictType 不变, dictSort/status/remark 等。
- **预期结果**：
  1. code=200，修改成功；详情/列表为新值。
- **依赖接口**：PUT /system/dict/data。

### DC-D22 字典数据-修改 dictSort
- **前置条件**：已存在数据。
- **步骤**：
  1. PUT /system/dict/data，body: dictCode, dictSort=10，其余不变。
- **预期结果**：
  1. code=200；/type/{dictType} 中该条排序位置变化。
- **依赖接口**：PUT /system/dict/data，GET /system/dict/data/type/{dictType}。

### DC-D23 字典数据-修改 status
- **前置条件**：已存在数据 status=0。
- **步骤**：
  1. PUT /system/dict/data，body: dictCode, status=1。
- **预期结果**：
  1. code=200，status=1；/type/{dictType} 可能不再返回该条（若只查 status=0）。
- **依赖接口**：PUT /system/dict/data。

### DC-D24 字典数据-修改不存在的 dictCode
- **前置条件**：已登录。
- **步骤**：
  1. PUT /system/dict/data，body: dictCode=999999, dictLabel=x, dictValue=x, dictType=某存在类型。
- **预期结果**：
  1. 返回 404 或业务错误。
- **依赖接口**：PUT /system/dict/data。

### DC-D25 字典数据-单条删除
- **前置条件**：已存在一条字典数据，dictCode 已知。
- **步骤**：
  1. DELETE /system/dict/data/{dictCode}。
- **预期结果**：
  1. code=200，删除成功；列表/详情/type 接口不再返回该条。
- **依赖接口**：DELETE /system/dict/data/{dictCodes}。

### DC-D26 字典数据-批量删除
- **前置条件**：已存在多条数据，dictCode 为 c1, c2, c3。
- **步骤**：
  1. DELETE /system/dict/data/c1,c2,c3。
- **预期结果**：
  1. code=200，三条均删除。
- **依赖接口**：DELETE /system/dict/data/{dictCodes}。

### DC-D27 字典数据-删除后列表不包含
- **前置条件**：已存在数据。
- **步骤**：
  1. DELETE /system/dict/data/{dictCode}；
  2. GET /system/dict/data/list 查询该类型。
- **预期结果**：
  1. 删除成功；
  2. rows 中无该 dictCode。
- **依赖接口**：DELETE，GET list。

### DC-D28 字典数据-删除后 type 接口不返回
- **前置条件**：已存在数据，且 /type/{dictType} 曾返回该条。
- **步骤**：
  1. DELETE /system/dict/data/{dictCode}；
  2. GET /system/dict/data/type/{dictType}。
- **预期结果**：
  1. 删除成功；
  2. 返回列表中无该 dictCode（缓存已刷新）。
- **依赖接口**：DELETE，GET /type/{dictType}。

### DC-D29 字典数据-删除不存在的 dictCode
- **前置条件**：已登录。
- **步骤**：
  1. DELETE /system/dict/data/999999。
- **预期结果**：
  1. 返回 404 或业务提示（视实现而定）。
- **依赖接口**：DELETE /system/dict/data/{dictCodes}。

### DC-D30 字典数据-导出
- **前置条件**：已登录，具备 system:dict:export。
- **步骤**：
  1. POST /system/dict/data/export，params 同列表（可选）。
- **预期结果**：
  1. HTTP 200，响应为 Excel 或流。
- **依赖接口**：POST /system/dict/data/export。

---

## 九、缓存与联动

### DC-C01 刷新字典缓存
- **前置条件**：已登录，具备 system:dict:remove（refreshCache 同权限）。
- **步骤**：
  1. DELETE /system/dict/type/refreshCache。
- **预期结果**：
  1. code=200，刷新成功。
- **依赖接口**：DELETE /system/dict/type/refreshCache。

### DC-C02 刷新缓存后 type 接口与库一致
- **前置条件**：已存在类型及数据；已修改某条数据未手动刷新。
- **步骤**：
  1. DELETE /system/dict/type/refreshCache；
  2. GET /system/dict/data/type/{dictType}。
- **预期结果**：
  1. 刷新成功；
  2. 返回数据与数据库一致。
- **依赖接口**：refreshCache，GET /type/{dictType}。

### DC-C03 类型修改 dictType 后数据与缓存一致
- **前置条件**：类型 A 下有数据；修改类型 A 的 dictType 为 B。
- **步骤**：
  1. PUT /system/dict/type 将 A 改为 B；
  2. GET /system/dict/data/type/B。
- **预期结果**：
  1. 修改成功；
  2. 原 A 的数据以 B 返回，缓存与库一致。
- **依赖接口**：PUT type，GET /type/{dictType}。

### DC-C04 数据新增后缓存包含新数据
- **前置条件**：已存在类型；新增一条数据。
- **步骤**：
  1. POST /system/dict/data 新增；
  2. GET /system/dict/data/type/{dictType}（不先 refreshCache）。
- **预期结果**：
  1. 新增成功；
  2. type 接口返回中包含新数据（若实现为写时更新缓存）。
- **依赖接口**：POST data，GET /type/{dictType}。

### DC-C05 数据删除后缓存更新
- **前置条件**：某类型下有数据，删除其中一条。
- **步骤**：
  1. DELETE /system/dict/data/{dictCode}；
  2. GET /system/dict/data/type/{dictType}。
- **预期结果**：
  1. 删除成功；
  2. type 接口不再返回该条。
- **依赖接口**：DELETE data，GET /type/{dictType}。

### DC-C06 类型删除后缓存移除
- **前置条件**：存在无数据的类型，删除该类型。
- **步骤**：
  1. DELETE /system/dict/type/{dictId}；
  2. GET /system/dict/data/type/原dictType。
- **预期结果**：
  1. 删除成功；
  2. type 接口返回空或该类型不存在（视实现）。
- **依赖接口**：DELETE type，GET /type/{dictType}。

---

## 十、权限与异常

### DC-E01 无 token 列表拒绝
- **前置条件**：未登录或 token 无效。
- **步骤**：
  1. GET /system/dict/type/list 不携带有效 token。
- **预期结果**：
  1. 返回 401 或 403。
- **依赖接口**：GET /system/dict/type/list。

### DC-E02 无 list 权限列表拒绝
- **前置条件**：已登录但无 system:dict:list。
- **步骤**：
  1. GET /system/dict/type/list。
- **预期结果**：
  1. 返回 403 或无权限提示。
- **依赖接口**：GET /system/dict/type/list。

### DC-E03 无 add 权限新增拒绝
- **前置条件**：已登录但无 system:dict:add。
- **步骤**：
  1. POST /system/dict/type 正常 body。
- **预期结果**：
  1. 返回 403 或无权限提示。
- **依赖接口**：POST /system/dict/type。

### DC-E04 无 edit 权限修改拒绝
- **前置条件**：已登录但无 system:dict:edit。
- **步骤**：
  1. PUT /system/dict/type 正常 body。
- **预期结果**：
  1. 返回 403 或无权限提示。
- **依赖接口**：PUT /system/dict/type。

### DC-E05 无 remove 权限删除拒绝
- **前置条件**：已登录但无 system:dict:remove。
- **步骤**：
  1. DELETE /system/dict/type/{dictId}。
- **预期结果**：
  1. 返回 403 或无权限提示。
- **依赖接口**：DELETE /system/dict/type/{dictIds}。

### DC-E06 无 export 权限导出拒绝
- **前置条件**：已登录但无 system:dict:export。
- **步骤**：
  1. POST /system/dict/type/export。
- **预期结果**：
  1. 返回 403 或无权限提示。
- **依赖接口**：POST /system/dict/type/export。

### DC-E07 数据列表无 list 权限拒绝
- **前置条件**：已登录但无 system:dict:list。
- **步骤**：
  1. GET /system/dict/data/list。
- **预期结果**：
  1. 返回 403 或无权限提示。
- **依赖接口**：GET /system/dict/data/list。

### DC-E08 optionselect 可无 list 权限访问
- **前置条件**：已登录但无 system:dict:list（若有权限控制）。
- **步骤**：
  1. GET /system/dict/type/optionselect。
- **预期结果**：
  1. 若接口设计为公开，则 code=200 返回列表；否则按实际权限设计。
- **依赖接口**：GET /system/dict/type/optionselect。

### DC-E09 type 接口可无 list 权限访问
- **前置条件**：已登录，无 system:dict:list。
- **步骤**：
  1. GET /system/dict/data/type/sys_user_sex。
- **预期结果**：
  1. 若接口不校验 list 权限，则 code=200 返回数据；否则 403。
- **依赖接口**：GET /system/dict/data/type/{dictType}。

### DC-E10 类型必填缺失返回校验错误
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body 缺少 dictName 或 dictType。
- **预期结果**：
  1. 返回 400 或 code 非 200，提示必填。
- **依赖接口**：POST /system/dict/type。

### DC-E11 数据必填缺失返回校验错误
- **前置条件**：已登录，已存在类型。
- **步骤**：
  1. POST /system/dict/data，body 缺少 dictLabel 或 dictValue 或 dictType。
- **预期结果**：
  1. 返回参数校验错误。
- **依赖接口**：POST /system/dict/data。

### DC-E12 超长字段返回校验错误
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，dictName 或 dictType 超过 100 字符。
- **预期结果**：
  1. 返回长度校验错误。
- **依赖接口**：POST /system/dict/type。

---

## 十一、非功能与边界（补充至 ≥100）

### DC-N01 类型列表 pageNum=0 或负数
- **前置条件**：已登录。
- **步骤**：
  1. GET /system/dict/type/list，params: pageNum=0 或 -1, pageSize=10。
- **预期结果**：
  1. 返回第一页或参数错误（视实现）。
- **依赖接口**：GET /system/dict/type/list。

### DC-N02 类型列表 total 与 rows 关系
- **前置条件**：已登录，total>0。
- **步骤**：
  1. GET /system/dict/type/list，pageSize=5。
- **预期结果**：
  1. len(rows)≤5，total≥len(rows)。
- **依赖接口**：GET /system/dict/type/list。

### DC-N03 数据列表 dictSort 排序
- **前置条件**：某类型下有多条数据，dictSort 不同。
- **步骤**：
  1. GET /system/dict/data/type/{dictType}。
- **预期结果**：
  1. 返回列表按 dictSort 升序（或业务约定）。
- **依赖接口**：GET /system/dict/data/type/{dictType}。

### DC-N04 类型新增带长 remark
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，dictName=测试, dictType=test_remark, remark=500字备注。
- **预期结果**：
  1. 若系统对 remark 无长度限制则成功；否则按限制返回。
- **依赖接口**：POST /system/dict/type。

### DC-N05 数据 label/value 100 字符边界
- **前置条件**：已存在类型；已登录。
- **步骤**：
  1. POST /system/dict/data，dictLabel 与 dictValue 各 100 字符。
- **预期结果**：
  1. 新增成功（边界内）。
- **依赖接口**：POST /system/dict/data。

### DC-N06 类型 dictType 下划线与数字
- **前置条件**：已登录。
- **步骤**：
  1. POST /system/dict/type，body: dictName=测试, dictType=sys_test_001。
- **预期结果**：
  1. code=200，符合 ^[a-z][a-z0-9_]*$。
- **依赖接口**：POST /system/dict/type。

---

## 用例汇总统计

| 章节 | 数量 |
|------|------|
| 一、字典类型-列表与查询 | 11 |
| 二、字典类型-新增 | 11 |
| 三、字典类型-修改 | 8 |
| 四、字典类型-删除 | 6 |
| 五、字典类型-导出与 optionselect | 3 |
| 六、字典数据-列表与查询 | 10 |
| 七、字典数据-新增 | 10 |
| 八、字典数据-修改与删除 | 10 |
| 九、缓存与联动 | 6 |
| 十、权限与异常 | 12 |
| 十一、非功能与边界 | 6 |
| **合计** | **93** |

为达到 ≥100 条，以下补充 7 条：

### DC-T40 字典类型-列表按创建时间范围
- **前置条件**：已登录。
- **步骤**：GET /system/dict/type/list，params: params[beginTime]、params[endTime]（若支持）。
- **预期结果**：code=200，rows 在时间范围内。
- **依赖接口**：GET /system/dict/type/list。

### DC-T41 字典类型-修改 dictType 格式不符合
- **前置条件**：已存在类型。
- **步骤**：PUT /system/dict/type，body: dictId, dictType=InvalidType。
- **预期结果**：返回格式校验错误。
- **依赖接口**：PUT /system/dict/type。

### DC-D31 字典数据-同一类型下多条 dictSort 顺序
- **前置条件**：同一类型下多条数据 dictSort 为 1,2,3。
- **步骤**：GET /system/dict/data/type/{dictType}。
- **预期结果**：返回顺序与 dictSort 一致。
- **依赖接口**：GET /system/dict/data/type/{dictType}。

### DC-D32 字典数据-新增不存在的 dictType
- **前置条件**：已登录。
- **步骤**：POST /system/dict/data，dictType=not_exist_type_xyz, dictLabel=l, dictValue=v。
- **预期结果**：返回错误（外键或业务校验）。
- **依赖接口**：POST /system/dict/data。

### DC-C07 刷新缓存后列表与库一致
- **前置条件**：先修改某类型名称，再刷新缓存。
- **步骤**：DELETE refreshCache；GET /system/dict/type/optionselect。
- **预期结果**：optionselect 中类型名称为最新。
- **依赖接口**：refreshCache，optionselect。

### DC-E13 数据无 add 权限新增拒绝
- **前置条件**：已登录但无 system:dict:add。
- **步骤**：POST /system/dict/data 正常 body。
- **预期结果**：返回 403。
- **依赖接口**：POST /system/dict/data。

### DC-N07 字典类型-删除后 refreshCache 仍成功
- **前置条件**：删除某类型后（或未删），调用刷新缓存。
- **步骤**：DELETE /system/dict/type/refreshCache。
- **预期结果**：code=200。
- **依赖接口**：DELETE /system/dict/type/refreshCache。

**最终合计：93 + 7 = 100 条测试用例。**
