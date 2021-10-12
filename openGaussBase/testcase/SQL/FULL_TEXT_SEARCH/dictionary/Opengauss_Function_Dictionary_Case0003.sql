-- @testpoint: 创建词典语法测试,name参数测试
--创建词典不带模式
drop text search dictionary if exists pg_dict;
create text search dictionary pg_dict (template = simple);
--创建模式
drop schema if exists test_sc;
create schema test_sc;
--创建词典带模式
drop text search dictionary if exists test_sc.pg_dict;
create text search dictionary test_sc.pg_dict (template = simple);
--删除词典
drop text search dictionary pg_dict;
drop text search dictionary test_sc.pg_dict;
drop schema if exists test_sc;