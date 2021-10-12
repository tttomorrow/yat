--  @testpoint:分别不指定模式，指定模式下创建序列
--创建序列，不指定模式，在当前模式（默认public）
drop SEQUENCE if exists serial;
CREATE SEQUENCE serial;
--创建模式
drop schema if exists test_schema cascade;
create schema test_schema;
--创建序列
drop SEQUENCE if exists test_schema.serial1;
CREATE SEQUENCE test_schema.serial1;
--查看序列信息
select sequence_name from test_schema.serial1 where sequence_name = 'serial1';
--删除序列
drop SEQUENCE serial;
drop SEQUENCE test_schema.serial1;
--删除schema
drop schema test_schema cascade;