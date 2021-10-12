-- @testpoint: opengauss关键字user(保留)，创建用户，验证基础功能正常

--创建用户，方式一，成功
drop user if exists user_test;
create user user_test password 'gauss@123';

--创建用户，方式二，成功
drop user if exists user_test;
create user user_test identified by 'gauss@123';

--创建有'创建数据库'权限的用户,成功
drop user if exists user_test;
create user user_test createdb password 'gauss@123';
drop user if exists user_test;
