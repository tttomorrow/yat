-- @testpoint: 设置temp_tablespaces为多个表空间空串，连续创建临时对象
--查看默认值
show temp_tablespaces;
--设置参数值
set temp_tablespaces to '','';
--查看
show temp_tablespaces;
--创建临时表
drop table if exists test_search_path046;
create temp table test_search_path046(i int);
drop table if exists test_search_path046_bak;
create temp table test_search_path046_bak(i int);
--查询(表空间为空)
select tablename ,tablespace from pg_tables where tablename = 'test_search_path046';
select tablename ,tablespace from pg_tables where tablename = 'test_search_path046_bak';
--恢复默认
set default_tablespace to '';
show default_tablespace;
--清理环境
drop table if exists test_search_path046;
drop table if exists test_search_path046_bak;
drop tablespace if exists t_tablespace046;
drop tablespace if exists t_tablespace046_bak;