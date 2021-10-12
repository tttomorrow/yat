--  @testpoint:opengauss关键字rename(非保留)，使用rename重命名
--TYPE
--创建一种复合类型，建表并插入数据以及查询
CREATE TYPE compfoo AS (f1 int, f2 text);
CREATE TABLE t1_compfoo(a int, b compfoo);
INSERT INTO t1_compfoo values(1,(1,'demo'));

--查询整个表
select * from t1_compfoo;

--查询表中b列第一个字段
SELECT (b).f1 FROM t1_compfoo;

--重命名数据类型
ALTER TYPE compfoo RENAME TO compfoo_1;

--查询重命名是否生效
select c.relname ,a.attname,t.typname
    from pg_class as c,pg_attribute as a,pg_type as t
    where relname = 't1_compfoo'
    and a.attname = 'b'
    and a.attrelid = c.oid
    and a.atttypid = t.oid;

--改变类型的名称或是一个复合类型中的一个属性的名称
ALTER TYPE compfoo_1 RENAME ATTRIBUTE  f2 TO bbb CASCADE;

--创建一个枚举类型
CREATE TYPE bugstatus AS ENUM ('create', 'modify', 'closed');

--重命名枚举类型的一个标签值
ALTER TYPE bugstatus RENAME VALUE 'create' TO 'new';

--清理环境
drop table t1_compfoo;
drop type compfoo_1;
drop type bugstatus;

--模式
--创建模式 moshi
CREATE SCHEMA moshi;
--重命名模式名
ALTER SCHEMA moshi RENAME TO moshi_new;

--清理环境
DROP SCHEMA moshi_new;

--Data Source
--创建一个空Data Source对象
CREATE DATA SOURCE ds_test1;

--修改名称
ALTER DATA SOURCE ds_test1 RENAME TO ds_test;

--清理环境
DROP DATA SOURCE ds_test;






