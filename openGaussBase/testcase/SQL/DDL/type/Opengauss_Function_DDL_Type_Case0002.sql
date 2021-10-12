--  @testpoint:创建复合类型，复合类型的列的现有数据类型为布尔类型
--创建一种复合类型
drop type if exists t_type2 cascade;
CREATE TYPE t_type2 AS (f1 boolean, f2 boolean);
--建表1
drop table if exists t1_test;
CREATE TABLE t1_test(a int, b t_type2);
--建表2
drop table if exists t2_test;
CREATE TABLE t2_test(a int, b t_type2);
--表1插入数据
INSERT INTO t1_test values(1,(TRUE,FALSE));
--表2插入数据
INSERT INTO t2_test select * from t1_test;
--查询全部
select * from t1_test;
--查询表1b字段的第一个值
select (b).f1 from t1_test;
--表1和表2联合查询
SELECT * FROM t1_test t1 join t2_test t2 on (t1.b).f1=(t2.b).f1;
--删除表
drop table t1_test;
drop table t2_test;
--删除复合类型
drop type t_type2 cascade;