--  @testpoint:创建数据库指定兼容的数据库类型是A
drop  database if exists t_test;
create database t_test DBCOMPATIBILITY='A';
drop  database t_test;