--  @testpoint:事务外，使用set..local SCHEMA 'schema'命令，设置schema为已存在的模式不会生效
--创建schema
 drop schema if exists myschema;
 create schema myschema;
 --set local SCHEMA为myschema
 set local SCHEMA 'myschema';
 --查询当前schema，还是public
 select current_schema;

 --set local schema为myschema，schema小写
 set local schema 'myschema';
 --查询当前schema，还是public
 select current_schema;
  drop schema myschema;