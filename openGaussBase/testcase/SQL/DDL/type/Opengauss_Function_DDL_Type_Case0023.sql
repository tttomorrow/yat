--  @testpoint:改变一种复合类型中某个属性的类型
--创建类型
drop type if exists test2_type cascade;
create type test2_type as(a int,b text);
--改变一种复合类型中某个属性的类型
ALTER TYPE test2_type ALTER ATTRIBUTE a SET DATA TYPE decimal(10,4);
--建表
drop table if exists test_t1 cascade;
create table test_t1 (id int,d test2_type);
--插入数据
insert into test_t1 values(1,(10.654,'hello'));
--查询
select * from test_t1;
--删除表
drop table if exists test_t1 cascade;
--删除类型
drop type if exists test2_type cascade;