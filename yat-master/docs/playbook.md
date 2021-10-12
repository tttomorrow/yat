# playbook

## 概述

`playbook`是`yat`框架提供的一种新的用例的编写和执行模式，用户可以将用例写在excel中，框架自动将excel中的用例生成文本用例并自动执行。

## 约束

- 编写的测试用例必须符合playbook用例规范
- Excel编码只支持utf-8编码

## Playbook用例编写规范

- 可以写多个excel SHEET页签
- 每个页签标记为一组相关用例
- 每个页签必须在第0行写上表头，其余每一行表示一个用例，表头模板见表3.1
- 标签顺序不敏感
- 支持配置页签，在配置页签中可以指定执行那些SHEET，配置页签名字必须为`configure`
- 可以在`macros`页签中定义宏变量
- 如果没有配置页签，默认第一个页签会被当做封面，或者自由格式的说明页签，被跳过，其他所有页签都被认为是一个测试用例集合

### 用例页签表头字段说明

#### POC 用例说明

##### 字段说明

- `Test Case Name`：测试用例名称，必须符合正则表达式：`[a-zA-Z0-9_-]+`
- `Test Case Setup`：测试用例的前置步骤，必须是一个yat可以支持的用例，如果不出现，则用例中没有Setup
- `Test Case Setp`：测试用例步骤，必须是一个yat可以解析的用例
- `Test Case Cleanup`：测试用例的后置步骤，必须是一个yat可以解析的用例，如果不出现，则用例中没有Cleanup
- `Test Case Expected`：用例正确时yat输出的文本结果，作为自动化对比参考
- `Test Case Output`：用于执行输出的回填，如果没有此字段不进行回填此字段
- `Test Case Result`：用于执行结果的回填，ok表示成功，failed表示失败，如果没有此字段不进行回填此字段
- `Test Case Execute Type`：当前支持`unit.sql` `z.sql` `sh`，分别表示单元测试sql用例、
    zsql用例、shell用例，没有此字段或者字段为空，默认为unit.sql
- `Test Case Automated`：只允许出现Y或者N，只有标记为Y的用例才会自动化运行

!!! Note

    **必须有的字段**：`Test Case Name`、`Test Case Setp`、`Test Case Expected`
    
    **选填字段**：其他字段

#### TMSS用例说明


##### 字段说明

- `Testcase Number`：测试用例名称，必须符合正则表达式：`[a-zA-Z0-9_-]+`
- `Testcase_Pretreatment Condition`：测试用例的前置步骤，必须是一个yat可以支持的用例，如果不出现，则用例中没有Setup
- `Testcase_Test Steps`：测试用例步骤，必须是一个yat可以解析的用例
- `Testcase Cleanup`：测试用例的后置步骤，必须是一个yat可以解析的用例，如果不出现，则用例中没有Cleanup
- `Testcase_Expected Result`：用例正确时yat输出的文本结果，作为自动化对比参考
- `Testcase_Outputt`：用于执行输出的回填，如果没有此字段不进行回填此字段
- `Testcase_Result`：用于执行结果的回填，ok表示成功，failed表示失败，如果没有此字段不进行回填此字段
- `Testcase Execute Type`：当前支持`unit.sql` `z.sql` `sh`，分别表示单元测试sql用例、
    zsql用例、shell用例，没有此字段或者字段为空，默认为unit.sql
- `Testcase_Automated`：只允许出现Y或者N，只有标记为Y的用例才会自动化运行

!!! Note

    **必须有的字段**：`Testcase Number`、`Testcase_Test Steps`、`Testcase_Expected Result` 
      
    **选填字段**：其他字段

### 配置页签表头字段说明

|sheet|execute|
|-----|-------|
|SHEET\_001|Y/N|
|SHEET\_002|Y/N|
|SHEET\_003|Y/N|

**必填字段**：`sheet`、`execute`

`sheet`：需要执行或禁止执行的页签名字

`execute`：只能是Y或者N，Y表示执行此页签下的自动化用例，N表示不执行

### 宏变量页签表头字段说明

|macro|value|
|-----|-----|
|macro1|value1|
|macro2|value2|
|macro3|value3|

**必填字段**：`macro`、`value`

`macro`：宏变量名字
`value`：宏变量值

## Yat支持语法说明

支持的语句：

- 任何sql语句
- Shell语句：`SHELL shell_command`
- `\!`语句：等价shell语句，建议用shell语句
- `conn`表达式：同`zsql conn`语句
- `reconnect`：重新连接数据
- `set autocommit on/off`语句

!!! Note

    每一个语句必须以分号结尾

## 命令行接口

### 如何选择excel用例格式

当前框架支持两种用例格式，分别是`poc`和`tmss`格式，那么如何指定要指向那种格式的playbook哪？

在命令行参数`-p`后面可以跟上一个路径指向一个playbook excel，此时默认使用tmss格式的用例，还可以指定一个url来指定路径和playbook格式

具体格式如下：

```text
url := <schema>:/path/to/playbook.xlsx

<schema> := tmss | poc

```

例如：

```bash
yat playbook [run] -p tmss:/path/to/playbook.xlsx
yat playbook [run] -p poc:/path/to/playbook.xlsx
```

### 执行playbook

执行一个`tmss`格式的excel并将执行结果和执行输出回填到新excel文件（playbook.result.xlsx）

```bash
yat playbook [run] –p playbook.xlsx
yat playbook [run] –p /path/to/playbook.xlsx

## or

yat playbook [run] -p tmss:playbook.xlsx
yat playbook [run] –p tmss:/path/to/playbook.xlsx
```

执行一个excel并将执行结果和执行输出回填到原excel文件

```bash
yat playbook [run] –p playbook.xlsx –force
```

### playbook生成测试套

将一个excel生成一个测试套，不执行，不回填执行结果

```bash
yat playbook gen –p playbook.xlsx
```

### 预期回填

回填预期到新的excel文件（playbook.back-fill.xlsx）

```bash
yat playbook bkfill –p playbook.xlsx
```

回填预期到原文件

```bash
yat playbook bkfill –p playbook.xlsx --force
```

### 配置node连接信息

指定node配置

```bash
yat playbook [run] –p playbook.xlsx –n nodes.yml
```
