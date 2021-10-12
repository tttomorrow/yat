--  @testpoint: 创建用户验证大小写
DROP schema if exists TEST_sensitive_52 cascade;
DROP USER TEST_sensitive_52 cascade;
DROP schema if exists TEST_sensitive_52 cascade;
create user TEST_sensitive_52 password '@123456qaz';
create user test_sensitive_52 password '@123456qaz';
grant all privileges to TeSt_sensitive_52;
DROP USER TEST_sensitive_52 cascade;
DROP USER test_sensitive_52 cascade;