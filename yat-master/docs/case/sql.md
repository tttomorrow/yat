# sql 用例编写规范

!!! Warning

    yat支持的sql，是标准SQL的超集，即在标准SQL的基础上进行了扩充，所有标准SQL都支持，扩展点在下面章节有详细说明
    
## 标准SQL用例编写

所有SQL都以`;`结尾，包括扩充的SQL语法。目标数据库支持的SQL都可以支持；存储过程等块儿SQL，以`/`结尾，`/`后面不需要再添加一个`;`，
与大部分数据库的SQL写法一致，这里不做过多说明。

## 用例结果打印说明

没有返回结果的`SQL`，如`DDL`，`DCL`等`SQL`，执行成功后直接打印`SQL SUCCESS`，如果`SQL`语句是一个查询，默认打印如下风格的输出

```text
select * from abc;

+----+------+-------------------------------+------------------------+
| ID | NAME | BORTH                         | IMG                    |
+----+------+-------------------------------+------------------------+
| 1  | abc  | 2018-01-01 00:00:00.000000000 | 334243bb234af234fbbc00 |
| 1  | abc  | 2020-01-01 00:00:00.000000000 | c8ff33                 |
| 2  | xxx  | 2020-02-01 00:00:00.000000000 | ffff33                 |
| 3  | ddd  | 2020-02-03 00:00:00.000000000 | 884433                 |
| 4  | ccc  | 2020-01-06 00:00:00.000000000 | 880033                 |
| 5  | fff  | 2020-01-03 00:00:00.000000000 | 889933                 |
| 6  | 23a  | 2020-01-04 00:00:00.000000000 | 8fff33                 |
| 7  | a23  | 2020-01-01 00:00:00.000000000 | 55ff33                 |
| 8  | 111  | 2020-01-01 00:00:00.000000000 | 00ff33                 |
| 1  | abc  | 2020-01-01 00:00:00.000000000 | c8ff33                 |
| 2  | xxx  | 2020-02-01 00:00:00.000000000 | ffff33                 |
| 3  | ddd  | 2020-02-03 00:00:00.000000000 | 884433                 |
| 4  | ccc  | 2020-01-06 00:00:00.000000000 | 880033                 |
| 5  | fff  | 2020-01-03 00:00:00.000000000 | 889933                 |
| 6  | 23a  | 2020-01-04 00:00:00.000000000 | 8fff33                 |
+----+------+-------------------------------+------------------------+
```

## 扩充的SQL语义

!!! Note

    扩充的`SQL`都有明显的标志就是关键字以`@`开头

举例：

```sql
create user abc identity by '';
grant dba to abc;

@connect abc/;

create table abc
(
    id int,
    name varchar(20),
    address varchar(1024),
    img varbinary(20000),
    birthday date
);

insert into abc values(?, ?, ?, ?, ?);

@batch
{
    int 1 str 'Javen' str 'Swordsman Museum' bytes '00FA303030CB' date '1991-01-22'
    int 2 str 'Alice' str 'Swordsman Museum' bytes 'EE23A303030CB' date '1991-01-23'
    int 3 str 'Kat' str 'Swordsman Museum' bytes 'FF23A303030CB' date '1991-01-24'
    int 4 str 'Kathleen' str 'Swordsman Museum' bytes '00FB00A303030CB' date '1991-01-25' 
}

select * from abc;

@set autocommit false;

insert into abc values(10, 'XX', 'None', '', '2020-1-1');

-- do not commit

@sh cm ctl stop -H all;
@sh cm ctl start -H all;

select * from abc;

```

上面例子中我们使用`@connnect`命令重新用新用例链接数据库，在建表完成后，使用`@batch`命令，执行批量绑定插入操作，通过`@set`命令设置默认提交，
通过`@sh`命令执行`shell`命令

所有的扩展命令说明如下：

### @set

执行设置命令，设置当前链接属性，可支持的链接属性设置如下

#### autocommit

设置当前链接是否自动提交

```sql
@set autocommit [true/false];
```

#### charset

设置当前编码格式

```sql
@set charset 'utf-8';
@set charset 'gbk'
```

#### echo

控制是否打印运行情况和输出

```sql
@set echo [true/false];  -- 所有输出全部打开/关闭
```

echo还可以指定子选项来控制命令回显、命令结果输出、注释信息输出等，见下面详细描述

##### echo result

控制执行结果是否输出

```sql
@set echo result [true/false];
```

##### echo statement

控制执行命令是否回显

```sql
@set echo statement [true/false];
```

##### echo comment

控制注释是否输出

```sql
@set echo comment [true/false];
```

### @connect/@conn

```sql
@conn/@connect user/password[@ip[:port]]
```

放弃当前链接，重新以新的用户链接数据，或者链接其他数据

例如：

重新以yat用户链接

```sql
@conn yat/;
```

重新以链接到备机

```sql
@conn yat/@192.168.1.2:4500;
```

重新以当前用来连接数据库

```sql
@conn;
```

### @desc/@describe

打印表的列值信息

### @bind

已绑定变量的方式执行SQL

例子：

```sql

select * from gcc where id > ? and name like ?;
 
@bind
{
	int 123 str abc
}

insert into table values(?, ?, ?);

@bind
{
	int 0 int 1 int 1
}
```

如果某个sql中带`?`即以绑定参数方式执行，语句后面需要紧跟一个`@bind`块儿，在块儿中输入绑定变量的类型和值

支持的数据类型如下,和对应常见数据库类型如下：

- str: varchar/char/nvarchar/varchar2/clob/text/longtext
- int: integer/int/smallint/tinyint
- long: bigint/long
- float: float
- double: double
- number: number/decimal
- bytes: blob/varbinary/binary/raw/image
- date: date
- time: time
- datetime: datetime/timestamp

### @batch

以批量绑定的方式执行SQL，此类SQL只能是无返回值的SQL，常见的如批量插入

例子：

```sql
insert into table values(?, ?, ?);

@batch
{
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
	int 0 int 1 int 1
}

```

批量插入数据11条

### @sh/@shell

执行本地`SHELL`命令

例如：

```sql
@sh zctl.py -t stop;
@sh zctl.py -t start;
```

通过上述操作重启`zenith`数据库，可以执行任意SQL，但是注意必须以`;`结尾，如果shell中有`;`，需要用`'`引用起来
例如：

```sql
@sh 'zctl.py -t stop; zctl.py -t start';
```

### @for

循环之下块儿中的语句

语法如下：

```sql
@for (count: 10 [timing: timing_name [timing_type: [sum/average]]])
{
    <statements>
}
```

`<statements>`可以是任何sql或者扩展的sql

例如：

测试两表关联查询10次数的平均耗时

```sql
@for (count: 10 timing: time_select, timing_type: average)
{
    select count(1) from 
    (
        select * from a, b 
        where 
            a.id = b.id and
            (a.cast > 0.2 or b.cast < 0.1) 
        group by a.name
    );
}
```

测试批量插入10条数据的总耗时

```sql
@for (count: 10 timing: time_batch, timing_type: sum)
{  
    insert into tbl_test values(?, ?, ?);
    @bind { int 1 str abc int 0 }
}
```

### @timing

计算块儿中语句执行耗时

### @compare

执行块儿中的groovy句子，返回true打印成功，否则打印失败

### @eval

执行块儿中groovy句子，打印返回结果
