-- @testpoint: 将sysadmin权限赋予指定的角色

drop user if exists user_017 cascade;
create user user_017 identified by 'Gauss_234';

grant all privileges to user_017;

revoke all privileges from user_017;
drop user if exists user_017;