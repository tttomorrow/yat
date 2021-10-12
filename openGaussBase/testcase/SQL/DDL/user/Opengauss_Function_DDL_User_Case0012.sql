-- @testpoint: 创建用户，参数REPLICATION | NOREPLICATION
--创建用户
drop user if exists test_user012 cascade;
create user test_user012 with REPLICATION identified by 'Test@123';
--查询用户信息
select rolname,rolreplication from pg_authid where rolname = 'test_user012';
--创建用户
drop user if exists test_user012 cascade;
create user test_user012 with noREPLICATION identified by 'Test@123';
--查询用户信息
select rolname,rolreplication from pg_authid where rolname = 'test_user012';
--删除用户
drop user if exists test_user012 cascade;
drop user if exists test_user012 cascade;