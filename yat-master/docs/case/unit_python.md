# python单元测试用例编写指导

!!! Warning

    虽然框架支持非单元测试（可以直接执行的）python用例，但是建议用户都使用python单元测试用例；python单元测试用例遵循所有的
    python单元测试用例规范，用例结构清晰，不建议使用非单元测试用例
    
    非单元测试用例编写规范见：[非单元测试用例规范](../python)
    
## 用例嵌套

!!! Warning

    单元测试用例不允许嵌套目录，将所有用例放到testcase目录下，这里你感觉可能不合理，用例很多怎么办？都放在一个目录里
    目录结构是不是不明晰？请看[这篇文章](../../advanced/case_layout)
    
    
## 单元测试用例基本要求

先看下面例子：

```python
from unittest import TestCase
from yat.test import Node

class TestSelect(TestCase):
    node = Node(node='default')

    def setUp(self):
        self.node.sql('select 1').success()

    def tearDown(self):
        self.node.sql('select 1').success()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_select_session(self):
        self.node.sql('select * from v$session').contains(
            ('1', '2', 'zsql', 'select * from v$session')
        )

    def test_restart_db(self):
        self.node.sh('zctl.py -t stop').success()
        self.node.sh('zctl.py -t start').success()

    def test_select_user_table(self):
        pass

    # ... other test case here

```

## Node 库参考

### 用例执行

#### Node.sh

在给定节点上执行shell命令

```python
Node.sh(cmd: str) => ShellResult
```

例子：

```python
import unittest
from yat.test import Node
import time

class TestRestart(unittest.TestCase):
    node = Node()

    def test_restart(self):
        node.sh('zctl.py -t stop; zctl.py -t start').success()

        while True:
            if node.sh('ps aux | grep zengine | grep -v grep').return_code() != 0:
                time.sleep(1)
                break
```

#### Node.scp_put

#### Node.scp_get

#### Node.sql

在给定节点上执行sql

```python
Node.sql(sql, *params) => SqlResult
```

#### Node.sqls

### 结果对比

#### BaseResult

SqlResult和ShellResult的基类， 主要方法如下

##### BaseResult.ands

##### BaseResult.ors

#### SqlResult

继承于BaseResult，方法如下

##### SqlResult.result

##### SqlResult.success

##### SqlResult.expect

##### SqlResult.error

##### SqlResult.contains

##### SqlResult.regex

##### SqlResult.rows

#### ShellResult

继承于BaseResult，方法如下

##### ShellResult.result

##### ShellResult.success

##### ShellResult.expect

##### ShellResult.return_code

##### SqlResult.contains

##### SqlResult.regex

##### SqlResult.code

##### SqlResult.not_code

