-- @testpoint: 使用set session...命令设置当前模式
--创建schema
drop schema if exists myschema;
create schema myschema;
--设置current_schema
set session current_schema =myschema;
--查看设置是否生效
select current_schema;
--查看该参数的具体运行信息
select * from pg_settings where name = 'current_schema';

--恢复current_schema为默认值
set session current_schema =default;
--查看系统表数据是否变化
select * from pg_settings where name = 'current_schema';
--查看当前schema，已恢复为默认public
select current_schema;
--清理环境
drop schema if exists myschema;


