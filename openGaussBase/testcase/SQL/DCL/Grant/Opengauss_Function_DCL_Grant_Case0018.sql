-- @testpoint: 回收角色上的sysadmin权限

drop user if exists user_018 cascade;
create user user_018 identified by 'Gauss_234';
grant all privileges to user_018;
revoke all privileges from user_018;
drop user if exists user_018;