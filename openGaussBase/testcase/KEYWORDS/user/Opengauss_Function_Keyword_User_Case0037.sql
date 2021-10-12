--  @testpoint:opengauss关键字user(保留)，修改用户信息

--前置条件
drop user if exists user_test;
create user user_test password 'gauss@123';

--修改用户名
alter user user_test rename to new_user_test;

--修改用户登录密码
alter user new_user_test identified by 'Gauss@123' replace 'gauss@123';

--为用户追加createrole权限
alter user new_user_test createrole;

--清空
drop user new_user_test cascade;