# 节点信息配置说明

!!! Note
    
    nodes.yml是yat中非常重要的一个配置文件，这个文件中定义了我们如何连接数据库，连接数据库的用户名密码IP端口等信息，
    同时配置了目标主机的ssh用户名密码，方便我们远程执行shell命令
    
    
## 节点信息配置详解

定义一个节点的方法如下

```yaml
# 定义链接zenith的节点
default:
  host: '127.0.0.1'
  db:
    type: 'zenith'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''

```

!!! Note

    注意`type`字段，此字段指明我们要定义的`node`链接zenith数据库，我们不需要写`url`和`driver`，yat知道默认的url和driver，
    但是如果需要自定义链接url，则定义如下
    
```yaml
# 定义链接zenith的节点，CN读写分离
default:
  host: '127.0.0.1'
  db:
    type: 'zenith'
    url: 'jdbc:zenith:db:@ip1:port1,ip2:port2?shardRwFlag=rw'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''
```

!!! Note

    这里不用写`driver`字段，因为定义了type字段，yat知道driver是什么

当前yat支持的type字段为：

1. zenith
2. postgresql
3. oracle

但是如果遇到了yat不支持type字段如何定义那？

我们这么定义：

```yaml
# 定义链接不直接支持的数据库，CN读写分离
default:
  host: '127.0.0.1'
  db:
    driver: 'org.xxx.xxx.XXXDriver'
    url: 'jdbc:xxx://${host}:${port}/dbname'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''
```

用户可以同时定义多个不同命的节点信息，例如定义三个节点信息：

```yaml
default:
  host: '127.0.0.1'
  db:
    type: 'zenith'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''

admin:
  host: '192.168.1.3'
  db:
    type: 'zenith'
    username: 'sys'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: root
    password: ''

normal:
  host: '192.168.1.3'
  db:
    type: 'zenith'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''

```

上面我们定义了3个节点，用户可以在用例中自由指定连接那个节点进行用例操作

!!! Warning

    如果版本是0.8.12或者以下版本，上述配置会报错，请修改为老版本的配置，0.8.12及以下版本都只支持老版本的配置文件，
    0.8.13及以上版本可以支持两种配置文件，但是未来会移除老版本的支撑，建议使用新版本的配置文件
    
**老版本的配置文件**

```yaml
-
  host: '127.0.0.1'
  name: default
  db:
    url: 'jdbc:zenith:@${host}:${port}'
    driver: 'com.huawei.gauss.jdbc.ZenithDriver'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''

-
  host: '192.168.1.3'
  name: admin
  db:
    url: 'jdbc:zenith:@${host}:${port}'
    driver: 'com.huawei.gauss.jdbc.ZenithDriver'
    username: 'sys'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: root
    password: ''

-
  host: '192.168.1.3'
  name: normal
  db:
    url: 'jdbc:zenith:@${host}:${port}'
    driver: 'com.huawei.gauss.jdbc.ZenithDriver'
    username: 'yat'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: yat
    password: ''

```

## yat指定默认加载节点

!!! Note

    yat默认会使用名字叫default的节点去做所有没有明确指定节点的用例操作，用户可以通过yat命令行中的-t参数指定默认使用哪个节点

例如

1) 默认使用default节点

```bash
yat suite run
```

2) 使用admin节点

```bash
yat suite run -t admin
```

## 在用例中指定使用哪个节点

### sql用例

```sql
@conn admin;
```

可以通过`conn node_name`的方式，指定使用指定名字的节点进行数据库重新链接

### shell用例

```bash
# 连接节点名字为default的节点，并执行sql语句
zsql $(node_conn default) -q -c "select * from v$session"

# 连接节点名字为admin的节点
zsql $(node_conn admin) -q -c "select * from v$session"
```

可以通过命令`node_conn <name>`获得给定节点名字zsql形式的连接字符串

### python用例

```python
from unittest import TestCase
from yat.test import Node


class TestSelect(TestCase):
    primary = None
    standby = None

    @classmethod
    def setUpClass(cls):
        self.primary = Node(node='primary')
        self.standby = Node(node='standby')

    def test_select_sessions(self):
        self.primary.sql('select * from v$session').count(200)
        self.standby.sql('select * from v$session').count(1)
        self.standby.shell('zctl.py -t stop')
```

通过`yat.test.Node`对象获取对应node名字的链接对象，并以此对象进行sql和shell操作

### zsql用例

!!! Note

    由于zsql用例的sql文本解析和执行都是有yat启动一个zsql子进程来执行的，不受yat控制，所以zsql用例只能通过conn命令进行数据库链接切换
    
```sql
conn ${DEFAULT_DB_USER}/${DEFAULT_DB_PASSWD}@${DEFAULT_DB_HOST}:${DEFAULT_DB_PORT}
conn ${ADMIN_DB_USER}/${ADMIN_DB_PASSWD}@${ADMIN_DB_HOST}:${ADMIN_DB_PORT}
```

!!! Note

    用户不需要自己在定义${DEFAULT_DB_USER} ${ADMIN_DB_PASSWD}等之类的宏变量了，系统默认会根据nodes.yml中的定义自动定义这些变量的
    见：[宏变量说明中的系统默认宏变量章节](../macro/#134)