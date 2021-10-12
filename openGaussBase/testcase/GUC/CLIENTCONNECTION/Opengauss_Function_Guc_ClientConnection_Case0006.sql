-- @testpoint: 使用ALTER SYSTEM SET方法设置search_path参数值，合理报错
--查看默认值
show search_path;
--创建模式
drop schema if exists t_myschema005 cascade;
create schema t_myschema005;
--修改参数值，报错
ALTER SYSTEM SET search_path to t_myschema005;
--清理环境
drop schema if exists t_myschema005 cascade;