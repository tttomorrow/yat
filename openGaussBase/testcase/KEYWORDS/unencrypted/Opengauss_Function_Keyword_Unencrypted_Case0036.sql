-- @testpoint: 修改用户指定密码存储不加密（合理报错）

drop user if exists encry_test;
create user encry_test with password 'Hello@123';
alter user encry_test with unencrypted password 'Hello+123';

--清理环境
drop user if exists encry_test;