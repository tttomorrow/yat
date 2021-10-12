--  @testpoint:用户组名长度测试
--用户组名超过63位，使用IDENTIFIED BY指定密码(截取前63位)
drop group if exists test_group1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap;
create group test_group1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap IDENTIFIED BY 'Xiaxia@123';
--使用64位group名称查询
select rolname from pg_authid where rolname = 'test_group1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap';
--使用63位group名称查询
select rolname from pg_authid where rolname = 'test_group1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
--删除group
drop group if exists test_group1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap;