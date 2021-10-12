-- @testpoint: 创建数据库使用指定表空间，合理报错

-- tblspace exists
drop tablespace if exists test_tblspc;
create tablespace test_tblspc RELATIVE LOCATION 'test_tblspc';
drop database if exists test_db;
create database test_db with TABLESPACE=test_tblspc;

-- tblspace is not exists
create database test_db1 with TABLESPACE='test_tblspc_not_exist';

--tearDown
drop database if exists test_db;
drop tablespace if exists test_tblspc;
