--  @testpoint:创建用户组，添加option选项，测试是否为sysadmin用户
--创建用户组，添加SYSADMIN
drop group if exists test_group1;
create group test_group1 with SYSADMIN PASSWORD 'Xiaxia@123';
--通过系统表查询是否为管理员
select rolname,rolsystemadmin from pg_authid where rolname = 'test_group1';
--创建用户组，添加NOSYSADMIN
drop group if exists test_group2;
create group test_group2 with NOSYSADMIN PASSWORD 'Xiaxia@123';
--通过系统表查询是否为管理员
select rolname,rolsystemadmin from pg_authid where rolname = 'test_group2';
--删除group
drop group test_group1;
drop group test_group2;