--  @testpoint:opengauss关键字user(保留)，删除用户

--带user关键字，成功
drop user if exists user_test cascade;
create user user_test password 'gauss@123';
drop user user_test;

--不带user关键字，失败
drop user_test;
