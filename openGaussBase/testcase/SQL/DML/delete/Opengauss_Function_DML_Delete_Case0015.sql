-- @testpoint: 删除表数据，目标表名有模式修饰，部分测试点合理报错
--创建schema
drop schema if exists test_schema cascade;
create schema test_schema;
--建表
drop table if exists test_schema.test_1t cascade;
create table test_schema.test_1t (id int,name varchar(20));
--插入数据
insert into test_schema.test_1t values(generate_series(1,100),'liyu');
--删除数据，表名不带模式，合理报错
delete from test_1t;
--删除数据，表名带模式，删除成功
delete from test_schema.test_1t;
--删除表
drop table test_schema.test_1t;
--删除schema
drop schema if exists test_schema cascade;