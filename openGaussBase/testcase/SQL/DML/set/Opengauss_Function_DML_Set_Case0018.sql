-- @testpoint: 使用set session...to命令设置当前模式
--创建schema
drop schema if exists myschema;
create schema myschema;
--设置schema为myschema
set session current_schema to myschema;
--查看当前schema
select current_schema;
--查看该参数值的具体运行信息
select * from pg_settings where name = 'current_schema';

--使用set default命令恢复current_schema参数默认值
set session current_schema to default;
--查看当前schema
select current_schema;
--清理环境
drop schema if exists myschema;