-- @testpoint: 修改用户名
-- @modified at: 2020-11-20
--创建用户
drop user if exists test_user007 cascade;
create user test_user007 identified by 'Tt@123456';
--修改用户名
ALTER USER test_user007 RENAME TO jimy;
--删除用户
drop user jimy;
