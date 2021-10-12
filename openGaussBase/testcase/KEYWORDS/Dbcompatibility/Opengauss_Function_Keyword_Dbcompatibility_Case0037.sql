--  @testpoint:创建数据库指定兼容的数据库类型是C
drop  database if exists t_test;
create database t_test DBCOMPATIBILITY='C';
drop  database t_test;