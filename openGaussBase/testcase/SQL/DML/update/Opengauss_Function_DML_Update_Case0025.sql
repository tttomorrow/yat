-- @testpoint: 修改的表名带模式修饰,修改成功
--创建模式
drop schema if exists test_schema;
create schema test_schema;
--建表
drop table if exists test_schema.test_update002;
create table test_schema.test_update002(c_integer integer, c_varchar varchar(50));
--插入数据
insert into test_schema.test_update002 values(1,'aaaaa');
insert into test_schema.test_update002 values(2,'bbbbb');
--修改数据
update test_schema.test_update002 set c_varchar = 'new_a' where c_integer = 1;
update test_schema.test_update002 set c_integer = c_integer+ 1 where c_varchar = 'bbbbb';
--查询
select * from test_schema.test_update002;
--删表
drop table test_schema.test_update002;
--删除模式
drop schema test_schema;
