-- @testpoint: set方法设置参数current_schema为有效值
--查看默认值
show current_schema;
--创建模式
drop schema if exists t_myschema021 cascade;
create schema t_myschema021;
--设置参数值
set current_schema to t_myschema021;
--查看
show current_schema;
--恢复默认
reset current_schema;
show current_schema;
--清理环境
drop schema if exists t_myschema021 cascade;