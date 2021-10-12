# Yat Quick Start

## 简介

!!! Note
 
    本文是Yat测试框架快速入门介绍，文中介绍了基本的安装方法，用例编写，调度文件编写，配置文件修改、JDBC驱动安装方法和用例执行，
    文中举一个测试zenith 逻辑导入导出lob类型特性的例子，初学者按照此例子可以进行简单用例编写和熟悉Yat框架。
    Yat只能在互信的环境中使用ssh。

## 安装

### 安装依赖

- Java 1.8+
- Python 3.6+

在执行安装前，请先安装上述依赖，yat提供两种安装方法，分别为在线安装和手动安装，推荐在线安装。

### 在线安装（推荐）

执行如下命令在线安装Yat：

```bash
bash <(curl -s install_yat.sh)
```

如果环境中已经安装了`Yat`，安装会报错，可以指定`-F`参数强制覆盖安装

```bash
bash <(curl -s install_yat.sh) -F
```

!!! Warning

    `-F`表示强制安装，如果环境中已经存在`-F`参数会先卸载旧版本Yat然后再执行安装
    
!!! Note

    yat依赖于python中的一些包，安装脚本会调用pip自动安装需要的依赖包，如果系统上没有安装pip，需要自行安装pip.


### 手工安装

#### 第一步

下载最新版本Yat安装包

```bash
wget yat-latest.tgz
```

#### 第二步

解压并执行安装脚本

```bash
tar xf yat-latest.tgz
cd yat-x.x.x
./install -F
```

## 创建测试套模板

Yat提供命令创建测试套模板，执行如下命令：

```bash
yat suite init -d test-suite-name
```

`test-suite-name`指要创建测试套目录名字，一般取要测试特性的名字，本文举例测试逻辑导入导出`lob`类型特性，执行如下命令：

```bash
yat suite init -d exp-imp-lob
```

此命令会在当前目录创建一个`exp-imp-lob`的目录，目录中已经存在若干目录和文件，此目录就是我们生成的测试套。

## 编写用例

执行完`yat init`命令后，指定的测试套目录下会有`testcase`目录，所有的测试用例都放在此目录下，支持的用例类型有：

### 通用用例类型

- sql用例， 以.sql结尾的用例
- shell用例，以.sh结尾的用例
- python单元测试用例，以.py结尾的用例
- python可执行用例，以.r.py结尾的用例
- groovy用例，以.groovy结尾的用例，且用例必须是一个junit用例

### zenith 独有用例类型

- zsql用例，以.z.sql结尾的用例，内部直接调用zsql执行此用例
- zsql交互式用例，以.iz.sql结尾的用例

!!! Note 

    为什么要有zsql用例和zsql交互式用例

    主要考虑以下几点：
    1） `zenith`中有很多功能性`SQL`是只能在`zsql`客户端中执行，如`exp`/`imp`/`load`/`dump`,此时如果用`shell`去调用`zsql`，
        用户会书写用例会比较繁琐；
    2） `zenith`中的`zsql`客户端工具有许多特性是`JDBC`无法承载的，如交互式绑定参数、server output等
    3） `JDBC`的连接存活检查机制会后台启动一个线程去连接数据库测试数据库是否有响应，这样导致部分在`nomount`模式的用例（restore/recover）无法执行，
        因为nomount模式只能有一个sys用户连接数据库，测试概率性JDBC的活性检查线程如果先链接上了数据库，会导致用例链接报错，不允许连接
    

用例的写法见用例书写相关章节

承接文中举例，我们做如下操作：

```bash
cd exp-imp-lob
touch testcase/create_user.sql
touch testcase/create_lob_data.py
touch testcase/exp.z.sql
touch testcase/imp.z.sql
```

每个文件内容如下：

create_user.sql:

```sql
@conn sys;
create user yat identified by '';
grant dba to yat;
```

create_lob_data.py:

```python
import unittest
from yat.test import Node

class CreateLobData(unittest.TestCase):
    node = Node()

    def test_create_lob_csv(self):
        self.node.sql('create table lob_tbl(a clob)')
        for _ in range(200):
            self.node.sql('insert into lob_tbl values(?)', ('0'*1000))
```

exp.z.sql:

```sql
exp table=lob_tbl file="temp/lob_bin_exp.dmp" filetype=bin parallel=3;
```

imp.z.sql:

```sql
imp file="temp/lob_bin_exp.dmp" filetype=bin table=lob_tbl;
```

上面我们创建了4个用例在testcase目录下，下一步是编写调度文件。

## 创建调度文件

执行完`yat init`命令后，指定的测试套目录下会有`conf`目录，创建`conf/schedule.schd`文件指定调度顺序，写法与`gs_regress`和`sqlc`相同，
详细用法参考[调度文件章节](config/schedule/#12-regression-format)

按文件举例修改调入文件如下：

**conf/schedule.schd**:

```text
test: create_user
test: create_lob_data
test: exp
test: imp
```

## 修改节点配置文件

Yat框架配置节点信息的文件为`conf/nodes.yml`，配置如下：

```yaml
# 配置默认节点，链接zenith数据库
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

# 配置数据库超级用户链接节点，链接zenith数据库
sys:
  host: '127.0.0.1'
  db:
    type: 'zenith'
    username: 'sys'
    password: ''
    port: 1611
  ssh:
    port: 22
    username: root
    password: ''
```

!!! Warning

    对于PG、MySQL或者其他数据库的链接配置方法见[节点配置文件章节](config/nodes)

!!! Warning

    如果版本是0.8.12或者以下版本，上述配置会报错，请修改为老版本的配置，0.8.12及以下版本都只支持老版本的配置文件，
    0.8.13及以上版本可以支持两种配置文件，但是未来会移除老版本的支撑，建议使用新版本的配置文件
    
**老版本nodes.yml配置文件**

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
  host: '127.0.0.1'
  name: sys
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
```
    

上述配置文件中配置了两个节点信息，都是连接本地节点，不同之处在于`sys`节点，
使用操作系统`root`用户进行`ssh`访问，使用数据库`sys`用户进行数据库访问，在`create_user.sql`用例中
使用`conn ${SYS_DB_USER}/${SYS_DB_PASSWD};`重新建立`sys`用户数据库链接。

可以配置多个节点的信息，至少需要配置`name`为`default`的节点

## 安装JDBC驱动

以在`zenith`数据库上执行为例，需要安装`zenith`的`JDBC`驱动，提供三种驱动安装方式。

### 方式一：局部安装

适用场景，只有一个测试套需要运行

在测试套根目录添加lib目录，并将驱动拷贝到此目录，注意驱动文件要有读权限

```bash
mkdir –p lib
cp /path/to/com.huwei.gauss.jdbc.ZenithDriver-XXX.jar lib
chmod a+r lib/*.jar
```

### 方式二：全局安装

试用场景，有多个测试套需要在同一个环境的同一个用户下运行

修改用户.bashrc文件，通过环境变量指定驱动搜索路径

```bash
mkdir –p ~/lib
cp /path/to/com.huwei.gauss.jdbc.ZenithDriver-XXX.jar ~/lib
chmod a+r ~/lib/*.jar
echo 'export YAT_LIB_PATH=$HOME/lib' >> ~/.bashrc
source ~/.bashrc
```

## 执行测试套

### 方式一

进入测试套根目录，并执行

```bash
cd exp-imp-lob
yat suite [run]
```

### 方式二

不在测试套根目录，通过命令行参数指定测试套路径执行

```bash
Yat suite [run] –d /data/gaussdba/testcase/exp-imp-lob
```

## 附录

### 常用操作命令

#### 查看yat帮助说明

```bash
yat –help
```

Yat子命令如init、schedule、run-test也都有自己的帮助命令，执行：

yat <sub-command\> --help查看具体信息，例如run-test子命令的帮助信息

```bash
yat suite --help
yat playbook --help
```

#### 查看yat版本

```bash
yat version
```
