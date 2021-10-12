-- @testpoint: 创建用户，默认具有登录权限以及创建同名schema
--创建用户
drop user if exists test_user001 cascade;
create user test_user001 identified by 'Tt@123456';
--查询用户的登录权限
select rolname,rolcanlogin from pg_authid where rolname = 'test_user001';
--查询是否有和用户同名的schema
select schema_name from information_schema.schemata where schema_name = 'test_user001';
--删除用户
drop user test_user001 cascade;
