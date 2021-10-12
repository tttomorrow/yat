-- @testpoint: 使用set session... SCHEMA 'schema'命令设置当前模式，schema为非字符串，合理报错
--创建schema
drop schema if exists myschema;
create schema myschema;
--设置schema为非字符串合理报错
set session schema myschema;
--清理环境
drop schema if exists myschema;


