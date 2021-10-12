--  @testpoint:创建数据库指定兼容的数据库类型是B
drop  database if exists t_test;
create database t_test DBCOMPATIBILITY='B';
drop  database t_test;