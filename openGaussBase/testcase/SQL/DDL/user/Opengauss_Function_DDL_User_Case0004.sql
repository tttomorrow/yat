-- @testpoint: 创建用户，AUDITADMIN | NOAUDITADMIN参数测试
--创建用户
drop user if exists test_user004 cascade;
create user test_user004 identified by 'Tt@123456';
--查询用户，默认不是审计用户
select rolname,rolauditadmin from pg_authid where rolname = 'test_user004';
--创建用户，指定为审计用户
drop user if exists test_user004_bak cascade;
create user test_user004_bak AUDITADMIN  identified by 'Tt@123456';
--查询用户
select rolname,rolauditadmin from pg_authid where rolname = 'test_user004_bak';
--创建用户，添加参数NOSYSADMIN
drop user if exists test_user004_bak1 cascade;
create user test_user004_bak1 NOSYSADMIN identified by 'Tt@123456';
--查询用户
select rolname,rolauditadmin from pg_authid where rolname = 'test_user004_bak1';
--删除用户
drop user if exists test_user004 cascade;
drop user if exists test_user004_bak cascade;
drop user if exists test_user004_bak1 cascade;




