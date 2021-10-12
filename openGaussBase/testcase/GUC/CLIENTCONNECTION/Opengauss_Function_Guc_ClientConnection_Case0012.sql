-- @testpoint: 将pg_temp模式加入search_path设为搜素路径最后位置,有告警提示;创建临时表，查询模式
--查看
show search_path;
--设置，弹出warning
set search_path to "$user",public,pg_temp;
--创建临时表
drop table if exists test_search_path012;
create temp table test_search_path012(id int);
--查询表模式，在pg_temp模式下
select schemaname,tablename from pg_tables where tablename = 'test_search_path012';
--清理环境
drop table if exists test_search_path012;
set search_path to "$user",public;