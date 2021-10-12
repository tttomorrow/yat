-- @testpoint: set方法设置参数default_tablespace为已存在的表空间，并在该表空间下建表
--查看默认值
show default_tablespace;
--创建表空间
drop tablespace if exists t_tablespace031;
create tablespace t_tablespace031 relative location 'tablespace/tablespace_1234';
--设置参数值
set default_tablespace to t_tablespace031;
--查看
show default_tablespace;
--指定表空间创建表
drop table if exists test_search_path031;
create table test_search_path031(i int) tablespace t_tablespace031;
--查询
select tablename ,tablespace from pg_tables where tablename = 'test_search_path031';
--恢复默认
set default_tablespace to '';
show default_tablespace;
--清理环境
drop table if exists test_search_path031;
drop tablespace if exists t_tablespace031;