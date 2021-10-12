-- @testpoint: 使用ALTER SYSTEM SET方法设置current_schema参数值，合理报错
--创建模式
drop schema if exists t_myschema022 cascade;
create schema t_myschema022;
--修改参数值，报错
ALTER SYSTEM SET current_schema to t_myschema022;
--清理环境
drop schema if exists t_myschema022 cascade;