-- @testpoint: 参数temp_tablespaces保持默认值，创建临时表，查询表空间为空
--查看默认值
show temp_tablespaces;
--创建临时表
drop table if exists test_search_path043;
create temp table test_search_path043(i int);
--查询
select tablename ,tablespace from pg_tables where tablename = 'test_search_path043';
--删表
drop table if exists test_search_path043;