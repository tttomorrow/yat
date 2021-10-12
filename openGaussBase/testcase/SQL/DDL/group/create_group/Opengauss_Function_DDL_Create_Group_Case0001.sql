--  @testpoint:创建新的用户组，用户组名测试
--符合标识符
drop group if exists test_group1;
create group test_group1 PASSWORD 'Xiaxia@123';
select rolname from pg_authid where rolname = 'test_group1';
--不符合标识符,合理报错
create group $#test_group1 PASSWORD 'Xiaxia@123';
--删除group
drop group test_group1;
