-- @testpoint: --创建表验证表名大小写敏感：合理报错
drop table if exists false_1 cascade;
drop table if exists falsE_1 cascade;
create table false_1(a int);
create table falsE_1(a int);
