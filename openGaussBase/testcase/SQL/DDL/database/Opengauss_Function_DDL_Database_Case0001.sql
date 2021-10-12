-- @testpoint: 创建数据库指定参数owner及template,合理报错

-- create database with specified owner
drop database if exists ts_test;
drop user if exists jim;
CREATE USER jim PASSWORD 'Bigdata@123';
CREATE DATABASE ts_test WITH OWNER = jim;

-- create database with template1:fail
drop database if exists ts_test;
CREATE DATABASE ts_test WITH TEMPLATE=template1;

-- create database with template0
drop database if exists ts_test;
CREATE DATABASE ts_test WITH TEMPLATE=template0;

--tearDown
drop database if exists ts_test;
drop user if exists jim;

