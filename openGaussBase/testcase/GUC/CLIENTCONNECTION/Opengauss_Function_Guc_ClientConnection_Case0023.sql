-- @testpoint: 设置current_schema为新模式，再新模式下建表查询
--查看默认值
show current_schema;
--创建模式
drop schema if exists t_myschema023 cascade;
create schema t_myschema023;
--设置新模式
set current_schema to t_myschema023;
show current_schema;
--建表
drop table if exists test_search_path023;
create table test_search_path023(id int);
--查询表的模式
select schemaname,tablename from pg_tables where tablename = 'test_search_path023';
--删表
drop table if exists test_search_path023;
reset current_schema;
show current_schema;
drop schema if exists t_myschema023 cascade;