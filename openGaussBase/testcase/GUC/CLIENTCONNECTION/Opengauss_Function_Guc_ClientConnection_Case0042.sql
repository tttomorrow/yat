-- @testpoint: set方法设置temp_tablespaces为已存在的名称，建表查询
--查看默认值
show temp_tablespaces;
--创建表空间
drop tablespace if exists t_tablespace042;
create tablespace t_tablespace042 relative location 'tablespace/tablespace_12';
--设置参数值
set temp_tablespaces to t_tablespace042;
--查看
show temp_tablespaces;
--指定表空间创建临时表
drop table if exists test_search_path042;
create temp table test_search_path042(i int) tablespace t_tablespace042;
--查询
select tablename ,tablespace from pg_tables where tablename = 'test_search_path042';
--恢复默认
set default_tablespace to '';
show default_tablespace;
--清理环境
drop table if exists test_search_path042;
drop tablespace if exists t_tablespace042;