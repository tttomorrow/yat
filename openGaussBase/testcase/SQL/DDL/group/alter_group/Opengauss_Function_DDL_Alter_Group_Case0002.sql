--  @testpoint:从用户组中删除用户
--创建用户组
drop group if exists test_group9;
create group test_group9 with sysadmin PASSWORD 'Xiaxia@123';
--创建用户
drop user if exists lche cascade;
create user lche PASSWORD 'Xiaxia@123';
drop user if exists jim cascade;
create user jim PASSWORD 'Xiaxia@123';
--向用户组中添加用户
ALTER GROUP test_group9 ADD USER lche, jim;
--查询系统表PG_AUTH_MEMBERS，之间的成员关系
select count(*) from PG_AUTH_MEMBERS where roleid = (select oid from pg_authid where rolname = 'test_group9') and member in(select oid from pg_authid where rolname in('lche', 'jim'));
--从用户组中删除用户
ALTER GROUP test_group9 DROP USER jim;
--查询系统表PG_AUTH_MEMBERS，之间的成员关系（只剩一个用户）
select count(*) from PG_AUTH_MEMBERS where roleid = (select oid from pg_authid where rolname = 'test_group9') and member in(select oid from pg_authid where rolname in('lche', 'jim'));
--删除group
drop group test_group9;
--删除用户
drop user lche cascade;
drop user jim cascade;