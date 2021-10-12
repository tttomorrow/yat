--  @testpoint:修改用户组的名称
--创建用户组
drop group if exists test_group9;
create group test_group9 with sysadmin PASSWORD 'Xiaxia@123';
--修改用户组的名称
drop group if exists new_test_group9;
ALTER GROUP test_group9 RENAME TO new_test_group9;
select rolname from pg_authid where rolname = 'new_test_group9';
--删除用户组
drop group new_test_group9;