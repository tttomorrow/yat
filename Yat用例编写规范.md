![avatar](./images/openGauss.png)

版权所有 © 2023 openGauss社区 您对“本文档”的复制、使用、修改及分发受知识共享(Creative Commons)署名—相同方式共享4.0国际公共许可协议(以下简称“CC BY-SA 4.0”)的约束。为了方便用户理解，您可以通过访问[*https://creativecommons.org/licenses/by-sa/4.0/*](https://gitee.com/link?target=https%3A%2F%2Fcreativecommons.org%2Flicenses%2Fby-sa%2F4.0%2F) 了解CC BY-SA 4.0的概要 (但不是替代)。CC BY-SA 4.0的完整协议内容您可以访问如下网址获取：[*https://creativecommons.org/licenses/by-sa/4.0/legalcode*](https://gitee.com/link?target=https%3A%2F%2Fcreativecommons.org%2Flicenses%2Fby-sa%2F4.0%2Flegalcode)。

## 1 通用规范

1）用例中命名规则：

- 用例名：Opengauss\_特性名\_Case00xx.sql/Opengauss\_特性名\_Case00xx.py
- 禁止出现有特殊含义的密码

- 类名使用大驼峰，如BigAuditFile
- 变量名、函数名小写，下划线连接，如avail_size
- 数据库相关变量命名
  - 表空间名：ts\_用例名
  - 表名：t\_[特性\_]用例名\_1、t\_[特性\_]用例名\_2
  - 索引名：i\_[特性\_]用例名\_1、i\_[特性\_]用例名\_2
  - 用户名：u\_[特性\_]用例名
  - 以此类推……

2）保证用例的独立性，除特殊情况外（如兼容性用例增加整体setup和teardown文件）， 每个用例都需要能单独执行

3）可提取的公共函数放到utils/xUtils

- utils中存放shell节点/数据库节点等公共方法
- xUtils中方法针对不同特性提取的公共方法

3）门禁为单机环境，若有非sql用例在主备环境才执行的，类定义时请参考如下处理：@unittest.skipIf(pri_sh.get_node_num()<=1,'单机环境不执行')

4）断言要精准，不可出现假通过，如self.assertIn('1', res)，数字1在多种场景都会出现，关键字信息不足。

5）python用例中，涉及路径的参数避免使用字符串拼接，用os.path.join()代替

6）不同场景结果不同且无特殊意义的输出语句，用正则进行模糊匹配，如Position数字、time时间等

## 2 sql用例代码编写规范

1）测试点中有ERROR报错语句时，-- @testpoint总述中需含有“合理报错”标识。

2）修改已合入用例，需添加 -- @history说明项

3）用例最后需清除掉创建的数据

用例模板见：

yat-master\template\testcase\Opengauss_template_include_error_Case0001.sql

yat-master\template\testcase\Opengauss_template_include_error_Case0001

yat-master\template\testcase\Opengauss_template_include_error_Case0002.sql

yat-master\template\testcase\Opengauss_template_include_error_Case0002

## 3 python用例代码编写规范

1）修改已合入用例，需添加 -- @history说明项

2）用例编写注意事项

- setup：初始化用到的节点信息等，记录需修改的参数的原始值，备份文件等
- test：添加必要的执行步骤说明，建议定义为 ---stepX：重要步骤描述---
- teardown：清理环境，包括删除创建的表、表空间等，恢复修改的参数，文件等；为了避免某一个断言校验失败，导致后续清理步骤无法执行，请在所有清理步骤完成后进行断言

用例模板见：

yat-master\template\testcase\Opengauss_template_Case0003.py

## 4 schedule命名规范

|    特性类    | schedule前缀 |              schedule具体名              |
| :----------: | :----------: | :--------------------------------------: |
|    接入层    |    FU_AC     |     JDBC<br />ODBC<br />GDBC<br />……     |
|    SQL层     |    FU_SQ     |   GRAM<br />KEYWORD<br />PROC<br />……    |
|    存储层    |    FU_ST     | FULLINDEX<br />MATER<br />USTORE<br />…… |
|  DFX-高可用  |    DF_HA     |         BACKUP<br />DUMP<br />……         |
|   DFX-管理   |    DF_MA     |          OM<br />TOOLS<br />……           |
|   DFX-性能   |    DF_PE     |               WDR<br />……                |
|   DFX-安全   |    DF_SE     |         AUDIT<br />MASK<br />……          |
|   硬件兼容   |    EC_HW     |               CPU<br />……                |
|    O*兼容    |    EC_OR     |             GRAMMAR<br />……              |
|    M*兼容    |    EC_MY     |       DATATYPE<br />PLUGIN<br />……       |
| 其他软件兼容 |    EC_SW     |               SYS<br />……                |

