-- @testpoint: 事务中，使用set..local命令，设置current_schema为已存在的模式,事务中生效
--创建schema
drop schema if exists myschema;
create schema myschema;
--开启事务
start transaction;
--set local to命令设置schema为myschema
set local current_schema to myschema;
--查询当前schema，由public更改为myschema
select current_schema;
--提交事务
commit;
--查询当前schema,恢复为默认public
select current_schema;


--再次开启事务
start transaction;
--set local =命令设置schema为myschema
set local current_schema = myschema;
--查询当前schema，由public更改为myschema
select current_schema;
--回滚
rollback;
--查询当前schema,又恢复为默认public
select current_schema;
--set session命令再次设置会话级别的模式
set session schema 'myschema';
--查询当前schema，会话级别命令生效，schema更改为myschema
select current_schema;
--恢复默认schema
reset current_schema;
--查询当前schema,恢复为public
select current_schema;

--清理环境
drop schema if exists myschema;