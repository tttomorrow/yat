-- @testpoint: 创建临时表使用default_tablespace参数值
--查看默认值
show default_tablespace;
--创建表空间
drop tablespace if exists t_tablespace032;
create tablespace t_tablespace032 relative location 'tablespace/tablespace_11';
--设置参数值
set default_tablespace to t_tablespace032;
--查看
show default_tablespace;
--指定表空间创建临时表
drop table if exists test_search_path032;
create temp table test_search_path032(i int) tablespace t_tablespace032;
--查询
select tablename ,tablespace from pg_tables where tablename = 'test_search_path032';
--恢复默认
set default_tablespace to '';
show default_tablespace;
--清理环境
drop table if exists test_search_path032;
drop tablespace if exists t_tablespace032;