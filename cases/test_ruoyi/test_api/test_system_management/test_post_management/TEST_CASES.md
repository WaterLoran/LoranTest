# 岗位管理测试用例（120+）

每个用例包含：用例编号、标题、前置条件、测试步骤、预期结果。

---

## A. 基础 CRUD（20 例）

### TC-A01 创建岗位-全部字段
- **前置条件**：已登录且具备岗位新增权限。
- **步骤**：1. 调用 POST /system/post，请求体：postName=测试岗位A，postCode=code_a_01，postSort=1，status=0，remark=备注A。2. 调用 GET /system/post/list，postName=测试岗位A。
- **预期结果**：步骤1 返回 code=200、msg=操作成功；步骤2 返回的 rows 中存在 postName=测试岗位A、postCode=code_a_01、postSort=1、status=0、remark=备注A。

### TC-A02 创建岗位-仅必填
- **前置条件**：已登录且具备岗位新增权限。
- **步骤**：1. 调用 POST /system/post，仅传 postName=必填岗、postCode=req_only、postSort=1，不传 status、remark。2. 查询该岗位详情。
- **预期结果**：步骤1 返回 code=200；详情中 status 为 0（默认正常），remark 为空或 null。

### TC-A03 查询列表-无筛选
- **前置条件**：系统中存在若干岗位。
- **步骤**：调用 GET /system/post/list，不传 postName、postCode、status，可传 pageNum=1、pageSize=10。
- **预期结果**：返回 code=200，包含 rows 数组和 total 字段，rows 为当前页岗位列表。

### TC-A04 查询列表-按名称
- **前置条件**：存在岗位名称为“经理岗”的岗位。
- **步骤**：调用 GET /system/post/list，postName=经理。
- **预期结果**：返回 code=200，rows 中每条记录的 postName 包含“经理”（或按后端 LIKE 规则匹配）。

### TC-A05 查询列表-按编码
- **前置条件**：存在岗位编码为“mgr”的岗位。
- **步骤**：调用 GET /system/post/list，postCode=mgr。
- **预期结果**：返回 code=200，rows 中每条 postCode 包含“mgr”（或按 LIKE 规则）。

### TC-A06 查询列表-按状态
- **前置条件**：存在状态为停用(status=1)的岗位。
- **步骤**：调用 GET /system/post/list，status=1。
- **预期结果**：返回 code=200，rows 中每条 status 均为 1。

### TC-A07 查询列表-组合条件
- **前置条件**：存在名称含“测试”且状态为正常的岗位。
- **步骤**：调用 GET /system/post/list，postName=测试，status=0。
- **预期结果**：返回 code=200，rows 中每条 postName 含“测试”且 status=0。

### TC-A08 查询岗位详情
- **前置条件**：已知有效岗位 ID（如 5）。
- **步骤**：调用 GET /system/post/5。
- **预期结果**：返回 code=200，data 中包含 postId、postName、postCode、postSort、status、remark 等完整信息。

### TC-A09 修改岗位-全部字段
- **前置条件**：已存在一个岗位（记 postId=P1）。
- **步骤**：调用 PUT /system/post，body 含 postId=P1，postName=新名称，postCode=new_code，postSort=10，status=1，remark=新备注。再 GET /system/post/P1。
- **预期结果**：PUT 返回 code=200、msg=操作成功；详情中名称、编码、顺序、状态、备注均为上述新值。

### TC-A10 修改岗位-部分字段
- **前置条件**：已存在岗位 P1（postName=A，postCode=c1，postSort=1）。
- **步骤**：调用 PUT /system/post，仅修改 postName=仅改名称，postId、postCode、postSort、status、remark 保持原值。再查详情。
- **预期结果**：postName 为新值，postCode、postSort、status、remark 与修改前一致。

### TC-A11 删除单个岗位
- **前置条件**：存在未分配用户的岗位 P1。
- **步骤**：1. 调用 DELETE /system/post/P1。2. 调用 GET /system/post/P1。
- **预期结果**：步骤1 返回 code=200、msg=操作成功；步骤2 返回错误或 404，或 data 为空。

### TC-A12 批量删除岗位
- **前置条件**：存在未分配用户的岗位 P1、P2。
- **步骤**：调用 DELETE /system/post/P1,P2。
- **预期结果**：返回 code=200、msg=操作成功；列表及详情中 P1、P2 均不存在。

### TC-A13 获取下拉选项
- **前置条件**：无。
- **步骤**：调用 GET /system/post/optionselect。
- **预期结果**：返回 code=200，data 为岗位数组（无分页），每项含 postId、postName、postCode 等。

### TC-A14 导出岗位-无筛选
- **前置条件**：无。
- **步骤**：调用 POST /system/post/export，不传筛选参数。
- **预期结果**：返回 HTTP 200，响应为 Excel 文件或流，可解析出岗位数据。

### TC-A15 导出岗位-有筛选
- **前置条件**：无。
- **步骤**：调用 POST /system/post/export，传入 postName=某名称 或 status=0。
- **预期结果**：返回 200，导出内容与筛选条件一致。

### TC-A16 完整生命周期
- **前置条件**：无。
- **步骤**：1. 创建岗位 A。2. 列表查询含 A。3. 详情查询 A。4. 修改 A 的名称与备注。5. 再次详情确认修改生效。6. 删除 A。7. 详情或列表确认 A 不存在。
- **预期结果**：每步接口返回成功，数据符合操作预期；删除后无法再查到 A。

### TC-A17 创建后立即查询
- **前置条件**：无。
- **步骤**：1. POST 创建岗位（唯一名称与编码）。2. 立即 GET /system/post/list 按名称筛选。
- **预期结果**：列表中出现刚创建的岗位，数据一致。

### TC-A18 修改后立即查询
- **前置条件**：存在岗位 P1。
- **步骤**：1. PUT 修改 P1 的 postName 与 remark。2. 立即 GET /system/post/P1。
- **预期结果**：详情返回修改后的 postName 与 remark。

### TC-A19 删除后查询详情
- **前置条件**：存在岗位 P1，已执行删除 P1。
- **步骤**：调用 GET /system/post/P1。
- **预期结果**：返回错误（如 code=500 或 404）或提示岗位不存在。

### TC-A20 空列表分页
- **前置条件**：筛选条件保证无匹配（如 postName=不可能存在的长随机串）。
- **步骤**：调用 GET /system/post/list，postName=该随机串，pageNum=1，pageSize=10。
- **预期结果**：code=200，rows 为空数组，total=0。

---

## B. 岗位名称验证（15 例）

### TC-B01 名称为空
- **步骤**：POST /system/post，postName=""，postCode=c1，postSort=1。
- **预期结果**：code=500 或 400，msg 含“岗位名称不能为空”。

### TC-B02 名称仅空格
- **步骤**：POST /system/post，postName="   "，postCode=c2，postSort=1。
- **预期结果**：根据后端是否 trim，返回“岗位名称不能为空”或创建成功（若 trim 后为空则报错）。

### TC-B03 名称1字符
- **步骤**：POST /system/post，postName=岗，postCode=c3，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-B04 名称50字符边界
- **步骤**：POST /system/post，postName 为 50 个字符（如 50 个“测”），postCode=c4，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-B05 名称51字符超长
- **步骤**：POST /system/post，postName 为 51 个字符，postCode=c5，postSort=1。
- **预期结果**：code=500 或 400，msg 含“岗位名称长度不能超过50个字符”或类似。

### TC-B06 名称中文
- **步骤**：POST /system/post，postName=高级工程师，postCode=c6，postSort=1。
- **预期结果**：code=200，列表/详情中 postName 正确显示。

### TC-B07 名称特殊字符
- **步骤**：POST /system/post，postName=测试!@#，postCode=c7，postSort=1。
- **预期结果**：根据业务规则，允许则 code=200，否则返回校验错误。

### TC-B08 名称数字
- **步骤**：POST /system/post，postName=12345，postCode=c8，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-B09 名称前后空格
- **步骤**：POST /system/post，postName="  名称  "，postCode=c9，postSort=1。
- **预期结果**：若后端 trim 则保存为“名称”；否则可能报错或保存带空格。

### TC-B10 名称换行符
- **步骤**：POST /system/post，postName="第一行\n第二行"，postCode=c10，postSort=1。
- **预期结果**：根据业务是否允许换行，返回成功或校验错误。

### TC-B11 名称HTML标签
- **步骤**：POST /system/post，postName="<script>alert(1)</script>"，postCode=c11，postSort=1。
- **预期结果**：根据转义策略，保存为转义后文本或拒绝。

### TC-B12 名称SQL注入尝试
- **步骤**：POST /system/post，postName="'; DROP TABLE sys_post;--"，postCode=c12，postSort=1。
- **预期结果**：不执行 SQL，可能保存为普通字符串或报错，系统安全。

### TC-B13 名称XSS尝试
- **步骤**：POST /system/post，postName="<img src=x onerror=alert(1)>"，postCode=c13，postSort=1。
- **预期结果**：不执行脚本，保存或转义处理。

### TC-B14 名称null
- **步骤**：POST /system/post，body 中不包含 postName 或 postName: null，postCode=c14，postSort=1。
- **预期结果**：code=500 或 400，提示岗位名称不能为空。

### TC-B15 名称超长500字符
- **步骤**：POST /system/post，postName 为 500 字符，postCode=c15，postSort=1。
- **预期结果**：code=500 或 400，提示长度不能超过 50 个字符。

---

## C. 岗位编码验证（15 例）

### TC-C01 编码为空
- **步骤**：POST /system/post，postName=名称，postCode=""，postSort=1。
- **预期结果**：code=500 或 400，msg 含“岗位编码不能为空”。

### TC-C02 编码仅空格
- **步骤**：POST /system/post，postName=名称，postCode="   "，postSort=1。
- **预期结果**：根据是否 trim，返回编码不能为空或成功。

### TC-C03 编码1字符
- **步骤**：POST /system/post，postName=名称，postCode=x，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-C04 编码64字符边界
- **步骤**：POST /system/post，postName=名称，postCode 为 64 字符，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-C05 编码65字符超长
- **步骤**：POST /system/post，postName=名称，postCode 为 65 字符，postSort=1。
- **预期结果**：code=500 或 400，msg 含“岗位编码长度不能超过64个字符”。

### TC-C06 编码纯数字
- **步骤**：POST /system/post，postName=名称，postCode=10086，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-C07 编码字母数字
- **步骤**：POST /system/post，postName=名称，postCode=code123，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-C08 编码下划线
- **步骤**：POST /system/post，postName=名称，postCode=code_ab，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-C09 编码中文
- **步骤**：POST /system/post，postName=名称，postCode=编码中文，postSort=1。
- **预期结果**：根据业务规则，允许则 code=200。

### TC-C10 编码特殊字符
- **步骤**：POST /system/post，postName=名称，postCode=code-1.2，postSort=1。
- **预期结果**：根据业务规则校验。

### TC-C11 编码前后空格
- **步骤**：POST /system/post，postName=名称，postCode="  code  "，postSort=1。
- **预期结果**：若 trim 则按“code”保存或唯一性校验；否则按带空格处理。

### TC-C12 编码null
- **步骤**：POST /system/post，不传 postCode 或 postCode: null，postName=名称，postSort=1。
- **预期结果**：code=500 或 400，岗位编码不能为空。

### TC-C13 编码大小写区分
- **步骤**：1. 创建岗位 postCode=Abc。2. 再创建 postCode=abc。
- **预期结果**：若唯一性区分大小写，则两个均可创建；否则第二个报编码已存在。

### TC-C14 编码与名称同值
- **步骤**：POST /system/post，postName=同一值，postCode=同一值，postSort=1。
- **预期结果**：若业务允许，code=200；否则按业务规则。

### TC-C15 编码超长128字符
- **步骤**：POST /system/post，postName=名称，postCode 为 128 字符，postSort=1。
- **预期结果**：code=500 或 400，提示编码长度不能超过 64 个字符。

---

## D. 显示顺序验证（10 例）

### TC-D01 postSort为0
- **步骤**：POST /system/post，postName=名称，postCode=c1，postSort=0。
- **预期结果**：code=200，创建成功，详情中 postSort=0。

### TC-D02 postSort正整数
- **步骤**：POST /system/post，postName=名称，postCode=c2，postSort=100。
- **预期结果**：code=200，创建成功。

### TC-D03 postSort最大值
- **步骤**：POST /system/post，postSort=2147483647（或后端允许最大值），其他必填有效。
- **预期结果**：根据字段类型，成功或溢出错误。

### TC-D04 postSort负数
- **步骤**：POST /system/post，postName=名称，postCode=c4，postSort=-1。
- **预期结果**：code=500 或 400，显示顺序校验失败。

### TC-D05 postSort空null
- **步骤**：POST /system/post，不传 postSort 或 postSort: null，postName=名称，postCode=c5。
- **预期结果**：code=500 或 400，显示顺序不能为空。

### TC-D06 postSort小数
- **步骤**：POST /system/post，postSort=1.5，postName=名称，postCode=c6。
- **预期结果**：根据后端类型，可能取整成功或报类型错误。

### TC-D07 postSort字符串
- **步骤**：POST /system/post，postSort="1"，postName=名称，postCode=c7。
- **预期结果**：根据反序列化规则，可能转为 1 成功或报错。

### TC-D08 列表按postSort排序
- **前置条件**：存在多条岗位，postSort 不同。
- **步骤**：GET /system/post/list，不筛选或筛选出多条。
- **预期结果**：返回的 rows 按 postSort 升序（或文档约定顺序）排列。

### TC-D09 修改postSort后排序
- **前置条件**：岗位 P1 当前 postSort=5。
- **步骤**：PUT 将 P1 的 postSort 改为 1。再 GET 列表。
- **预期结果**：列表中 P1 的排序位置变化，按新 postSort 排列。

### TC-D10 postSort相同多岗位
- **步骤**：创建两个岗位，postSort 均为 10，名称编码不同。
- **预期结果**：均创建成功；列表展示时顺序稳定（如按 id 二次排序）。

---

## E. 状态验证（8 例）

### TC-E01 status为0正常
- **步骤**：POST /system/post，postName=名称，postCode=c1，postSort=1，status=0。
- **预期结果**：code=200，详情/列表中 status=0。

### TC-E02 status为1停用
- **步骤**：POST /system/post，postName=名称，postCode=c2，postSort=1，status=1。
- **预期结果**：code=200，详情/列表中 status=1。

### TC-E03 status无效值2
- **步骤**：POST /system/post，postName=名称，postCode=c3，postSort=1，status=2。
- **预期结果**：code=500 或 400，或保存为默认/拒绝。

### TC-E04 status空字符串
- **步骤**：POST /system/post，status=""，其他必填有效。
- **预期结果**：根据默认值或校验，成功为 0 或报错。

### TC-E05 status非数字
- **步骤**：POST /system/post，status=正常，其他必填有效。
- **预期结果**：code=500 或 400，类型或枚举校验错误。

### TC-E06 正常改停用
- **前置条件**：岗位 P1 状态为 0。
- **步骤**：PUT /system/post，postId=P1，status=1，其他保持不变。
- **预期结果**：code=200，详情中 status=1。

### TC-E07 停用改正常
- **前置条件**：岗位 P1 状态为 1。
- **步骤**：PUT /system/post，postId=P1，status=0。
- **预期结果**：code=200，详情中 status=0。

### TC-E08 下拉选项含状态
- **步骤**：GET /system/post/optionselect。
- **预期结果**：返回的岗位列表中每项包含 status 或仅返回正常岗位，符合接口文档。

---

## F. 备注验证（8 例）

### TC-F01 备注为空
- **步骤**：POST /system/post，postName=名称，postCode=c1，postSort=1，remark=""。
- **预期结果**：code=200，详情中 remark 为空。

### TC-F02 备注可选不传
- **步骤**：POST /system/post，不传 remark，其他必填有效。
- **预期结果**：code=200，remark 为空或 null。

### TC-F03 备注500字符边界
- **步骤**：POST /system/post，remark 为 500 字符，其他必填有效。
- **预期结果**：code=200，保存成功。

### TC-F04 备注501字符超长
- **步骤**：POST /system/post，remark 为 501 字符，其他必填有效。
- **预期结果**：若后端限制 500，则 code=500 或 400；否则按实际限制。

### TC-F05 备注特殊字符
- **步骤**：POST /system/post，remark=备注!@#\$%，其他必填有效。
- **预期结果**：code=200，回显正确。

### TC-F06 备注中文
- **步骤**：POST /system/post，remark=这是中文备注，其他必填有效。
- **预期结果**：code=200，回显正确。

### TC-F07 备注换行
- **步骤**：POST /system/post，remark="第一行\n第二行"，其他必填有效。
- **预期结果**：code=200，保存与展示正确。

### TC-F08 备注null
- **步骤**：POST /system/post，remark: null，其他必填有效。
- **预期结果**：code=200，按空处理；或根据实现报错。

---

## G. 唯一性约束（12 例）

### TC-G01 新增重复岗位名称
- **前置条件**：已存在岗位 postName=经理。
- **步骤**：POST /system/post，postName=经理，postCode=other_code，postSort=1。
- **预期结果**：code=500，msg 含“岗位名称已存在”或“新增岗位'经理'失败，岗位名称已存在”。

### TC-G02 新增重复岗位编码
- **前置条件**：已存在岗位 postCode=mgr。
- **步骤**：POST /system/post，postName=其他名称，postCode=mgr，postSort=1。
- **预期结果**：code=500，msg 含“岗位编码已存在”或类似。

### TC-G03 修改为已存在名称
- **前置条件**：岗位 P1 名称=A1；岗位 P2 名称=A2。
- **步骤**：PUT 将 P1 的 postName 改为 A2（与 P2 重复）。
- **预期结果**：code=500，msg 含“岗位名称已存在”或“修改岗位'A2'失败，岗位名称已存在”。

### TC-G04 修改为已存在编码
- **前置条件**：岗位 P1 编码=c1，岗位 P2 编码=c2。
- **步骤**：PUT 将 P1 的 postCode 改为 c2。
- **预期结果**：code=500，msg 含“岗位编码已存在”或类似。

### TC-G05 名称唯一编码不同可新增
- **前置条件**：已存在岗位（名称=N1，编码=C1）。
- **步骤**：POST /system/post，postName=N2，postCode=C2，postSort=1。
- **预期结果**：code=200，创建成功（验证名称与编码均唯一才可新增）。

### TC-G06 编码唯一名称不同可新增
- **前置条件**：已存在岗位（名称=N1，编码=C1）。
- **步骤**：POST /system/post，postName=N2，postCode=C2，postSort=1。
- **预期结果**：code=200，创建成功。

### TC-G07 修改保持自身名称
- **前置条件**：岗位 P1 名称=原名称，编码=c1。
- **步骤**：PUT /system/post，仅修改 remark，postName、postCode 保持原名称、c1。
- **预期结果**：code=200，不因“与自身重复”而报错。

### TC-G08 修改保持自身编码
- **前置条件**：同上。
- **步骤**：PUT 仅修改 postSort，postCode 保持 c1。
- **预期结果**：code=200，保存成功。

### TC-G09 同名称不同编码两条
- **步骤**：创建岗位（名称=同名，编码=c1）。再创建（名称=同名，编码=c2）。
- **预期结果**：第二笔应失败，岗位名称已存在（名称唯一）。

### TC-G10 同编码不同名称不允许
- **步骤**：创建岗位（名称=N1，编码=同码）。再创建（名称=N2，编码=同码）。
- **预期结果**：第二笔失败，岗位编码已存在。

### TC-G11 名称大小写是否区分
- **步骤**：创建岗位 postName=Abc，postCode=c1。再创建 postName=abc，postCode=c2。
- **预期结果**：若名称唯一性区分大小写，则都成功；若不区分，第二笔报名称已存在。

### TC-G12 删除后同名可再创建
- **前置条件**：创建岗位（名称=再建，编码=del1）。删除该岗位。
- **步骤**：再次 POST 创建岗位（名称=再建，编码=del1），postSort=1。
- **预期结果**：code=200，允许再创建。

---

## H. 删除约束（8 例）

### TC-H01 删除未分配岗位
- **前置条件**：存在未分配任何用户的岗位 P1。
- **步骤**：DELETE /system/post/P1。
- **预期结果**：code=200，msg=操作成功；该岗位不再存在。

### TC-H02 删除已分配用户岗位应失败
- **前置条件**：岗位 P1 已分配给至少一个用户。
- **步骤**：DELETE /system/post/P1。
- **预期结果**：code=500，msg 含“已分配,不能删除”及岗位名称（如“董事长已分配,不能删除”）。

### TC-H03 批量删除全未分配
- **前置条件**：岗位 P1、P2 均未分配用户。
- **步骤**：DELETE /system/post/P1,P2。
- **预期结果**：code=200，两个岗位均被删除。

### TC-H04 批量删除含已分配
- **前置条件**：P1 未分配，P2 已分配。
- **步骤**：DELETE /system/post/P1,P2。
- **预期结果**：根据实现，可能整体失败并提示 P2 已分配；或部分成功（仅删 P1），需与产品一致。

### TC-H05 删除不存在ID
- **步骤**：DELETE /system/post/999999（不存在的 postId）。
- **预期结果**：返回错误（如 code=500 或 404），不抛未捕获异常。

### TC-H06 删除ID为0
- **步骤**：DELETE /system/post/0。
- **预期结果**：返回错误或未找到。

### TC-H07 删除负数ID
- **步骤**：DELETE /system/post/-1。
- **预期结果**：返回参数错误或 404。

### TC-H08 删除非数字ID
- **步骤**：DELETE /system/post/abc（若路径允许）或传非法参数。
- **预期结果**：返回 400 或 404，不执行删除。

---

## I. 分页（10 例）

### TC-I01 默认分页
- **步骤**：GET /system/post/list，不传 pageNum、pageSize。
- **预期结果**：code=200，返回第一页，每页条数为默认（如 10），含 total。

### TC-I02 自定义pageSize
- **步骤**：GET /system/post/list，pageNum=1，pageSize=5。
- **预期结果**：code=200，rows 长度不超过 5，total 为总记录数。

### TC-I03 页码超出总页
- **前置条件**：总记录 10 条，pageSize=10。
- **步骤**：GET /system/post/list，pageNum=5，pageSize=10。
- **预期结果**：code=200，rows 为空或最后一页数据，total=10。

### TC-I04 页码0或负
- **步骤**：GET /system/post/list，pageNum=0 或 -1，pageSize=10。
- **预期结果**：根据实现，报错或按 pageNum=1 处理。

### TC-I05 pageSize为1
- **步骤**：GET /system/post/list，pageNum=1，pageSize=1。
- **预期结果**：code=200，rows 长度不超过 1。

### TC-I06 pageSize极大
- **步骤**：GET /system/post/list，pageSize=99999。
- **预期结果**：根据后端限制，可能截断为最大 pageSize 或报错。

### TC-I07 total总数正确
- **前置条件**：已知某筛选条件下实际应有 N 条。
- **步骤**：GET /system/post/list，该筛选条件，pageSize 足够大或查多页汇总。
- **预期结果**：total=N，与预期一致。

### TC-I08 多页数据不重复
- **步骤**：GET pageNum=1、pageSize=2 与 pageNum=2、pageSize=2，对比 rows 中的 postId。
- **预期结果**：两页的 postId 无重复。

### TC-I09 pageSize为0
- **步骤**：GET /system/post/list，pageSize=0。
- **预期结果**：根据实现，报错或使用默认 pageSize。

### TC-I10 首页末页一致性
- **前置条件**：总数为 25，pageSize=10。
- **步骤**：取第 1 页与第 3 页，第 3 页应为 5 条。
- **预期结果**：total=25，第 3 页 rows 长度为 5。

---

## J. 组合筛选（8 例）

### TC-J01 仅名称
- **步骤**：GET /system/post/list，postName=某值。
- **预期结果**：rows 中每条 postName 匹配（如 LIKE）。

### TC-J02 仅编码
- **步骤**：GET /system/post/list，postCode=某值。
- **预期结果**：rows 中每条 postCode 匹配。

### TC-J03 仅状态
- **步骤**：GET /system/post/list，status=0。
- **预期结果**：rows 中每条 status=0。

### TC-J04 名称加状态
- **步骤**：GET /system/post/list，postName=测试，status=0。
- **预期结果**：rows 中每条名称含“测试”且 status=0。

### TC-J05 编码加状态
- **步骤**：GET /system/post/list，postCode=code，status=1。
- **预期结果**：rows 中每条编码含“code”且 status=1。

### TC-J06 名称加编码
- **步骤**：GET /system/post/list，postName=A，postCode=B。
- **预期结果**：rows 同时满足名称与编码条件。

### TC-J07 名称编码状态全选
- **步骤**：GET /system/post/list，postName=x，postCode=y，status=0。
- **预期结果**：rows 同时满足三个条件。

### TC-J08 条件无匹配结果
- **步骤**：GET /system/post/list，postName=不可能存在的唯一串，postCode=不可能存在。
- **预期结果**：code=200，rows=[]，total=0。

---

## K. 边界与异常（10 例）

### TC-K01 修改不存在岗位
- **步骤**：PUT /system/post，postId=999999，postName=x，postCode=y，postSort=1。
- **预期结果**：code=500 或 404，提示岗位不存在或操作失败。

### TC-K02 详情不存在岗位
- **步骤**：GET /system/post/999999。
- **预期结果**：返回错误或 data 为空。

### TC-K03 创建缺postName
- **步骤**：POST /system/post，不传 postName，postCode=c，postSort=1。
- **预期结果**：code=500 或 400，岗位名称不能为空。

### TC-K04 创建缺postCode
- **步骤**：POST /system/post，postName=n，不传 postCode，postSort=1。
- **预期结果**：code=500 或 400，岗位编码不能为空。

### TC-K05 创建缺postSort
- **步骤**：POST /system/post，postName=n，postCode=c，不传 postSort。
- **预期结果**：code=500 或 400，显示顺序不能为空。

### TC-K06 修改缺postId
- **步骤**：PUT /system/post，不传 postId，只传 postName、postCode、postSort。
- **预期结果**：code=500 或 400，参数错误或岗位 ID 缺失。

### TC-K07 非法JSON请求体
- **步骤**：POST /system/post，Content-Type=application/json，body 为非 JSON 字符串。
- **预期结果**：返回 400 或解析错误。

### TC-K08 列表非法pageNum
- **步骤**：GET /system/post/list，pageNum=abc。
- **预期结果**：根据实现，报错或按默认 1 处理。

### TC-K09 列表非法pageSize
- **步骤**：GET /system/post/list，pageSize=abc。
- **预期结果**：根据实现，报错或使用默认 pageSize。

### TC-K10 删除空ID
- **步骤**：DELETE /system/post/（路径为空）或 ID 为空。
- **预期结果**：返回 404 或 400，不执行删除。

---

## L. 数据完整性（6 例）

### TC-L01 创建后createBy createTime
- **步骤**：创建岗位后查询详情或列表。
- **预期结果**：数据中含 createBy、createTime，且 createTime 为当前合理时间。

### TC-L02 修改后updateBy updateTime
- **步骤**：修改岗位后查询详情或列表。
- **预期结果**：含 updateBy、updateTime，且 updateTime 晚于 createTime。

### TC-L03 修改单字段其它不变
- **前置条件**：岗位 P1 已知全部字段值。
- **步骤**：仅 PUT 修改 remark，其他不传或传原值。
- **预期结果**：仅 remark 变化，postName、postCode、postSort、status 不变。

### TC-L04 列表与详情数据一致
- **步骤**：从列表取某条 postId，再 GET 详情。
- **预期结果**：详情与列表中该条除列表未返回字段外一致。

### TC-L05 下拉与列表数据一致
- **步骤**：GET optionselect 与 GET list（无分页或大 pageSize）对比同一条岗位。
- **预期结果**：同 postId 的 postName、postCode 等一致。

### TC-L06 导出与列表数据一致
- **步骤**：相同筛选条件下导出与列表查询。
- **预期结果**：导出中的岗位集合与列表（含分页）数据一致。

---

**合计：A20 + B15 + C15 + D10 + E8 + F8 + G12 + H8 + I10 + J8 + K10 + L6 = 120 个测试用例**
