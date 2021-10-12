-- @testpoint: 使用set session... SCHEMA 'schema'命令设置当前模式
--创建schema
drop schema if exists myschema;
create schema myschema;
--设置schema
set session SCHEMA 'myschema';
--查询当前schema为myschema
select current_schema;
--查看该参数运行时的具体信息，user型参数
select * from pg_settings where name = 'current_schema';
--恢复current_schema默认值
reset current_schema;
--查看当前schema为public
select current_schema;
--清理环境
drop schema if exists myschema;