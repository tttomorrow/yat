-- @testpoint: 将视图的访问权限赋予指定的用户或角色

drop user if exists user_012 cascade;
create user user_012 identified by 'Gauss_234';

drop database if exists ts_test;
create database ts_test;

grant all privileges on database ts_test to user_012;
revoke all privileges on database ts_test from user_012;

drop user if exists user_012;
drop database if exists ts_test;