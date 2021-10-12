-- @testpoint: 将函数的访问权限赋予给指定的用户或角色

drop user if exists user_019 cascade;
create user user_019 identified by 'Gauss_234';

drop schema if exists test;
create schema test;

grant execute on all functions in schema test to user_019;
revoke all privileges from user_019;

drop schema test;
drop user user_019;