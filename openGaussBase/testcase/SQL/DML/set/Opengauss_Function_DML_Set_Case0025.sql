--  @testpoint:事务外，使用set..local命令，设置current_schema为已存在的模式不会生效
--创建schema
 drop schema if exists myschema;
 create schema myschema;
 --set local to命令设置当前模式为myschema
 set local current_schema to myschema;
 --查看当前模式，还是默认public模式
 select current_schema;

 --set local =命令设置当前模式为myschema
 set local current_schema = myschema;
 --查看当前模式，还是默认public模式
 select current_schema;

 --set local to default命令设置当前模式为myschema
 set local current_schema to default;
 --查看当前模式，还是默认public模式
 select current_schema;

--set local = default命令设置当前模式为myschema
 set local current_schema = default;
 --查看当前模式，还是默认public模式
select current_schema;
drop schema myschema;
