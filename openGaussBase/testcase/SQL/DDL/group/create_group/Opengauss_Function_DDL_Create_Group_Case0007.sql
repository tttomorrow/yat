--  @testpoint:创建用户组，添加option选项，测试用户是否允许流复制或设置系统为备份模式
drop group if exists test_group7;
create group test_group7 with REPLICATION PASSWORD 'Xiaxia@123';
--查询test_group7角色是否为一个复制的角色
select rolname,rolreplication from pg_authid where rolname = 'test_group7';
--创建用户组，添加NOREPLICATION
drop group if exists test_group8;
create group test_group8 with NOREPLICATION PASSWORD 'Xiaxia@123';
--查询test_group7角色是否为一个复制的角色
select rolname,rolreplication from pg_authid where rolname = 'test_group8';
--删除group
drop group test_group7;
drop group test_group8;