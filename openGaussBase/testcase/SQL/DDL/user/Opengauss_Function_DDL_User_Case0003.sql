-- @testpoint: 创建用户，SYSADMIN | NOSYSADMIN参数测试
--创建用户
drop user if exists test_user003 cascade;
create user test_user003 identified by 'Tt@123456';
--查询用户，默认不是管理员用户
select rolname,rolsystemadmin from pg_authid where rolname = 'test_user003';
--创建用户，指定为管理员用户
drop user if exists test_user003_bak cascade;
create user test_user003_bak sysadmin identified by 'Tt@123456';
--查询用户
select rolname,rolsystemadmin from pg_authid where rolname = 'test_user003_bak';
--创建用户，添加参数NOSYSADMIN
drop user if exists test_user003_bak1 cascade;
create user test_user003_bak1 NOSYSADMIN identified by 'Tt@123456';
--查询用户
select rolname,rolsystemadmin from pg_authid where rolname = 'test_user003_bak1';
--删除用户
drop user if exists test_user003 cascade;
drop user if exists test_user003_bak cascade;
drop user if exists test_user003_bak1 cascade;