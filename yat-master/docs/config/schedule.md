# Yat 调度文件语法和功能说明

!!! Note

    Yat执行测试套时需要指定调度文件来按用户指定的调度逻辑执行，下面介绍了两种当前支持的`Yat`调度文件

## 概述

`Yat`执行测试套时需要指定调度文件来按用户指定的调度逻辑执行，当前`Yat`支持两种调度文件格式：

1. `Regression Format`
2. `Yat Format`

下面分别对两种调度文件格式进行语法和功能说明

## Regression Format

Regression 格式的调度文件是从 Regression 框架沿袭过来的，调度文件优点简单易懂，缺点也很明显对于较大的调度文件，文件会很长，前后逻辑关系混乱，缺乏灵活性。

Yat在此基础上进行了扩展和和功能丰富，下面进行说明。

### 原始 Regression 格式调度文件语法

```text
test: test_case_001 test_case_002
test: test_case_003
test: test_case_004 test_case_005 test_case_006
```

**语法要点**：

- 一组用例写在 `test：` 后面，同一组用例必须写在**同一行**，用例之间用空格划分
- 多组用例串行列出

**功能要点**：

- 同一组用例并行执行
- 组与组之间按照先后顺序串行执行

### Yat 扩展后的 Regression 格式调度文件语法

扩展后的语法兼容`Regression`格式语法，同时提供两级语法支持

#### level 1

```text
setup: setup_case_001(valid = false) setup_case_002(valid = false)
macro: DB_USER test_user1
group: test_case_001 test_case_002
group: test_case_003(diff = false valid=false)
group: test_case_004 test_case_005
       test_case_006 test_case_007
       test_case_007 test_case_008

import: sub-suite.schd
cleanup: cleanup_case

```

**语法要点**：

- 每组用例用 `group:` 开头，当然老版本的 `test:` 开头依然支持，但是建议都用 `group:` 开头，**用例之间可以任意换行**
- `setup` 用例组表示一个测试套中的前置用例
- `cleanup` 用例组表示一个测试套中的后置清理用例
- `macro` 标签不是一个用例组，表示一个宏变量定义
- `import` 标签不是一个用例组，表示导入子调度文件
- 用例名字后面括号中的键值对（`valid = false diff=false`）表示用例属性，一个用例可以有多组属性，或者没有属性

**功能要点**：

- `setup` 用例组无论放到哪里都会**最先**执行
- `cleanup` 用例无论放到哪里都会**最后**执行
- `macro` 标签配置的宏变量可以在本组用例中使用
- `import` 导入的子调度文件

#### level 2

```text
name: user_without_grant
setup: setup_case_001(valid = false) setup_case_002(valid = false)
macro: DB_USER test_user1
group: test_case_001 test_case_002
group: test_case_003(diff = false)
group: test_case_004 test_case_005 test_case_006
import: sub-suite.schd

------

name: user_with_grant
setup: setup_case_003(valid = false)
macro: DB_USER test_user2
group: test_case_001 test_case_002
group: test_case_003(diff = false)
group: test_case_004 test_case_005 test_case_006
import: sub-suite.schd
group: test_case_100
cleanup: cleanup_case
```

在`level 1`的基础上，用户可以指定`name`选项，指定子测试套名称，并通过`------`分隔开两个子测试套

## Yat Format
