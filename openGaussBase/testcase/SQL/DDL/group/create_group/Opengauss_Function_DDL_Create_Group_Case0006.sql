--  @testpoint:创建用户组，添加option选项，测试用户是否具有审计管理属性
--创建group，添加AUDITADMIN
drop group if exists test_group5;
create group test_group5 with AUDITADMIN PASSWORD 'Xiaxia@123';
--查询test_group4是否具有审计管理属性
select rolname,rolauditadmin from pg_authid where rolname = 'test_group5';
--创建group，添加NOAUDITADMIN
drop group if exists test_group6;
create group test_group6 with NOAUDITADMIN PASSWORD 'Xiaxia@123';
--查询test_group4是否具有审计管理属性
select rolname,rolauditadmin from pg_authid where rolname = 'test_group6';
--删除group
drop group test_group5;
drop group test_group6;