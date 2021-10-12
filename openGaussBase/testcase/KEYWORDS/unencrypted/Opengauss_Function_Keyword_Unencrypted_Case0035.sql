--  @testpoint:创建用户指定密码存储不加密（合理报错）

drop user if exists encry_test;
create user encry_test with unencrypted password 'gauss@123';
