# LoranTest

## 作者前言

欢迎随时提issue， 相关问题可包括，培训，框架思路，分享沙龙等。
项目迭代缓慢的最重要的原因就是没有issue， 不知道大家的诉求， 所以只有大家踊跃提issue（代码问题， 项目期望， 培训期望等）， 咱们项目才能做得更好
当然也欢迎，大家使用我的框架，一起参与到该项目的自动化脚本的编写中来。
所以，请提issue

## 概况

支持接口自动化，web_ui自动化，app_ui自动化，未来将支持性能可靠性自动化，等其他功能

### 框架核心功能

1. 支持日志功能，日志能自动归档到执行目录
2. 支持报告功能，并支持钉钉等发送到通知群
3. 未来将具体支持各类配置，并提供示例
4. 未来将具体支持资源，并提供示例

### 接口自动化

1. 三层解耦，即数据层，逻辑层，业务层解耦
2. 支持函数式编程，代码简洁清晰，便于复制粘贴
3. 逻辑层的原理是，在api数据的基础上，增加入参解析填充功能，和响应信息提取的功能

### WEB_UI自动化

1. 支持执行时候自动截图，并归档到日志目录下
2. 支持PO模式，并提供示例

### APP_UI自动化

1. 支持PO模式，并提供示例

### 其他插件

1. 发送钉钉通知到通知群

## 框架说明
### 代码目录说明
1. cases目录: 用于存放接口自动化的用例, web_ui自动化的用例, 以未来的所有用例
2. common目录: 用于存放接口自动化的关键字, 即主要是APi数据层的接口描述
3. config目录: 用于存放配置, 包括环境配置, 飞书相关信息的配置, 框架的一些定制的配置, 以及未来的所有配置
4. core目录: 用于存放框架核心, 即框架分层的代码实现, 日志,报告,配置功能的实现, 以及发送接受请求, 断言和提取响应信息的代码实现
5. page目录: 用于存放page页面的定位元素描述, 不同页面的描述会依据于页面的结构去存放
6. plugin目录: 用于存放插件的目录, 即不属于框架的代码, 比如飞书通知, logic信息整理等一些非常规的代码

## 学习示例

1. 提供mysql联表查询示例
   脚本在case->test_mysql->query_mysql目录下
