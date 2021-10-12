-- @testpoint: set方法设置参数search_path为有效值
--查看默认值
show search_path;
--创建模式
drop schema if exists t_myschema004 cascade;
create schema t_myschema004;
--设置参数值
set search_path to t_myschema004;
--查看
show search_path;
--恢复默认
set search_path to "$user",public;
show search_path;
--清理环境
drop schema if exists t_myschema004 cascade;