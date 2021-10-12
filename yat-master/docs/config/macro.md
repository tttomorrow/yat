# Yat宏系统

## 配置文件位置

宏配置文件只能配置在`conf/macro.yml`中，用户通过`key-value`的方式指定变量值

!!! Note

    为了兼容老版本的yat测试套，支持java properties文件形式的宏配置文件，但是在未来版本可能移除这种兼容支持

## 使用方法

!!! Note

    yat宏系统中的宏变量可以在用例和期望文件中使用

### 在用例中

主要分为两种情况

* 如`sql`脚本等没有类型系统等的专用语言宏变量通过字符替换实现
* 如`shell`、有变量概念的语言，宏变量通过环境变量的形式注入
* 如`python`、`groovy`等高级语言，宏变量通过提高宏变量包库的形式读取宏变量

例如，如果定义宏配置文件如下：

```yaml
COMMON_PATH: temp/test_path

```

#### 在sql用例中

```sql
select * from tbl_test where path like '%${COMMON_PATH}%';
```

#### 在python用例中

```python
from unittest import TestCase
from yat.test import Node
from yat.test import macro


class TestMacro(TestCase):
    node = None

    @classmethod
    def setUpClass(cls):
        self.node = Node()
 
    def test_select(self):
        sql = 'select * from tbl_test where path like '%{}%'.format(macro.COMMON_PATH)
        self.node.sql(sql).expect(
            (0, 'abc', 34, 'temp/test_path'),
            (1, 'bcx', 35, 'temp/test_path'),
        )
```

#### 在shell用例中

```bash
zsql ${DEFAULT_DB_USER}/${DEFAULT_DB_PASSWD}@${DEFAULT_DB_HOST}:${DEFAULT_DB_PORT} \
    -c "select * from tbl_test where path like '%${COMMON_PATH}%' 
```

### 在期望文件中

例如上述SQL用例的期望文件查询结果中带`${COMMON_PATH}`变量的实际值，如果环境或者路径改变，期望文件也会频繁修改，为了应对这种情况我们可以在
期望文件中使用宏变量来消除这种路径依赖

```test
select * from tbl_test where path like '%${COMMON_PATH}%';

ID | NAME  | MARK | PATH                |
-----------------------------------------
0    abc    34     ${COMMON_PATH}
1    bcx    35     ${COMMON_PATH}

```

## Yat系统默认定义的宏

### RUN_SUITE

表示当前执行的测试套名称，如果有子测试套，就是子测试套的名称

### YAT_SUITE_DIR

表示当前测试套根目录的绝对路径

### YAT_SUITE_TEMP

表示当前测试套根目录下的temp目录的绝对路径

### 节点信息

在`nodes.yml`中配置的每一个节点信息都会对应9个宏变量如下：

!!! Note

    `nodes.yml`和节点等概念见章节[nodes配置章节](../nodes)

- <NODE_NAME\>_DB_USER
- <NODE_NAME\>_DB_PASSWD
- <NODE_NAME\>_DB_HOST
- <NODE_NAME\>_DB_PORT
- <NODE_NAME\>_DB_URL
- <NODE_NAME\>_DB_NAME

- <NODE_NAME\>_SSH_USER
- <NODE_NAME\>_SSH_PASSWD
- <NODE_NAME\>_SSH_HOST
- <NODE_NAME\>_SSH_PORT

这里面的`<NODE_NAME>`表示nodes.yml中定义的节点的名字

例如nodes.yml中有如下定义

```yaml
default:
  host: '127.0.0.1'
  db:
    url: 'jdbc:zenith:@${host}:${port}'
    driver: 'com.huawei.gauss.jdbc.ZenithDriver'
    username: 'yat'
    dbname: 'dbname'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''

sys:
  host: '127.0.0.1'
  db:
    url: 'jdbc:zenith:@${host}:${port}'
    driver: 'com.huawei.gauss.jdbc.ZenithDriver'
    username: 'sys'
    password: ''
    dbname: 'dbname'
    port: 1611
  ssh:
    port: 22
    username: root
    password: ''
```

则默认会定义如下宏变量

```yaml
DEFAULT_DB_USER: yat
DEFAULT_DB_PASSWD: ''
DEFAULT_DB_HOST: 127.0.0.1
DEFAULT_DB_PORT: '1611'
DEFAULT_DB_URL: 'jdbc:zenith:@${host}:${port}'
DEFAULT_DB_DBNAME: 'dbname'

DEFAULT_SSH_USER: yat
DEFAULT_SSH_PASSWD: ''
DEFAULT_SSH_HOST: 127.0.0.1
DEFAULT_SSH_PORT: 22

SYS_DB_USER: sys
SYS_DB_PASSWD: ''
SYS_DB_HOST: 127.0.0.1
SYS_DB_PORT: '1611'
SYS_DB_URL: 'jdbc:zenith:@${host}:${port}'
SYS_DB_DBNAME: 'dbname'

SYS_SSH_USER: root
SYS_SSH_PASSWD: ''
SYS_SSH_HOST: 127.0.0.1
SYS_SSH_PORT: 22
```