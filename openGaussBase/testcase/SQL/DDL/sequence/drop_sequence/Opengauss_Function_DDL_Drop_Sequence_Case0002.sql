-- @testpoint: 删除序列名带模式
--创建模式
drop schema if exists t_schema;
create schema t_schema;
--创建序列
drop SEQUENCE if exists t_schema.t_serial;
CREATE SEQUENCE t_schema.t_serial START 101;
--删除带模式的序列
drop SEQUENCE t_schema.t_serial;
--删除带模式的不存在序列，添加if exists，发出notice
drop SEQUENCE if exists t_schema.t_serial;
drop schema t_schema;
