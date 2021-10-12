--  @testpoint:删除类型，类型有依赖对象（表字段)
--创建一种复合类型
drop type if exists t_type4 cascade;
CREATE TYPE t_type4 AS (f1 int, f2 varchar2(20));
--建表1
drop table if exists t1_test;
CREATE TABLE t1_test(a int, b t_type4);
--插入数据
insert into t1_test values(1,(1,'helloworld'));
--删除类型不加cascade，合理报错
drop type t_type4;
--删除类型不加cascade，合理报错
drop type t_type4 RESTRICT;
--删除类型添加cascade，删除成功
drop type t_type4 cascade;
--删除表
drop table t1_test;