-- @testpoint: 创建复合类型，指定模式 合理报错
--创建模式
drop schema if exists test_schema;
create schema test_schema;
--创建一种复合类型,指定模式
drop TYPE if exists test_schema.compfoo cascade;
CREATE TYPE test_schema.compfoo AS (f1 int, f2 text);
--删除类型不带模式，合理报错
drop TYPE compfoo;
--删除类型带模式，删除成功
drop TYPE test_schema.compfoo;
--清理环境
drop schema if exists test_schema;