--  @testpoint:一个语句中同时增加多个属性
--创建类型
drop type if exists t_compfoo cascade;
CREATE TYPE t_compfoo AS (f1 int, f2 text);
--给复合类型增加新的属性
ALTER TYPE t_compfoo ADD ATTRIBUTE f3 numeric, add ATTRIBUTE f4 text,add ATTRIBUTE f5 decimal(10,4);
--建表
drop table if exists test_1 cascade;
create table test_1(a t_compfoo);
--插入数据
insert into test_1 values((1,'lily',1.578,'hello',10.895878));
--删除表
drop table test_1 cascade;
--删除类型
drop type t_compfoo cascade;