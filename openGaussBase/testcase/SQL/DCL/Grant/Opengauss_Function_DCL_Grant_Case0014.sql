-- @testpoint: 将模式的访问权限赋予指定的用户或角色

drop user if exists user_014 cascade;
create user user_014 identified by 'Gauss_234';
drop schema if exists test;
create schema test;

grant create on schema test to user_014;

revoke all privileges on schema test from user_014;

drop schema if exists test;
drop user if exists user_014;