-- @testpoint: 默认搜索路径下，建表，查询所属模式
--查看默认值
show search_path;
--建表
drop table if exists test_search_path007;
create table test_search_path007(id int);
--查询表的模式
select schemaname,tablename from pg_tables where tablename = 'test_search_path007';
--删表
drop table if exists test_search_path007;