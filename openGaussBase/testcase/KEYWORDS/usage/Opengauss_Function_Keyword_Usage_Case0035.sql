-- @testpoint: usage赋权（对象权限），验证功能正常

drop schema if exists usage_schema;
create schema usage_schema;
drop user if exists usage_test;
create user usage_test password 'gauss@123';
grant usage on schema usage_schema to usage_test;
revoke usage on schema usage_schema from usage_test;
drop schema if exists usage_schema;
drop user if exists usage_test;