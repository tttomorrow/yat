-- @testpoint: 根据用户名创建模式，合理报错
--1.create user:success
create user user_schema with password "Mima@123";
--2.create schema with exists user:success
CREATE SCHEMA schema_1 AUTHORIZATION user_schema;
--3.create schema with user which is not exists:fail
CREATE SCHEMA test AUTHORIZATION user_schema1;
CREATE SCHEMA AUTHORIZATION  user_schema1;
--4.create schema:success
create schema schema_2;
--5.create user:fail
create user schema_2 with password "Mima@123";
--6.rename user_schema:success
alter schema user_schema rename to user_schema1;
--7.create schema without schema name:success
CREATE SCHEMA AUTHORIZATION  user_schema;
--8.create role:success
CREATE ROLE  role1_schema IDENTIFIED BY 'Mima@123';
--9.create schema without schema name:success
CREATE SCHEMA AUTHORIZATION  role1_schema;
--10.create user named pg_xxx
create user pg_test with password "Mima@123";

--tearDown
drop schema if exists schema_2;
drop schema if exists schema_1;
drop schema if exists user_schema;
drop schema if exists role1_schema;
drop schema user_schema1;
drop user if exists user_schema;
drop role if exists role1_schema;
