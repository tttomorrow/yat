-- @testpoint: 创建视图,视图名添加模式修饰
--创建schema
drop schema if exists test_schema_006 cascade;
create schema test_schema_006;
--建表
drop table if exists table_view_006 cascade;
create table table_view_006(id int,name varchar(20));
--创建视图
drop view if exists test_schema_006.temp_view_006 cascade;
create view test_schema_006.temp_view_006 as select * from table_view_006;
--查询，无数据
select * from test_schema_006.temp_view_006;
--删除视图
drop view test_schema_006.temp_view_006;
--删表
drop table table_view_006;
drop schema test_schema_006 cascade;