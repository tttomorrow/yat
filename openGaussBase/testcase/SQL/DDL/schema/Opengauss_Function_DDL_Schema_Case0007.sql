-- @testpoint: 删除模式,合理报错
drop schema if exists test_case007;
drop schema test_case007;
create schema test_case007;
create table test_case007.i_tbl(i int);
drop schema test_case007;
drop schema test_case007 restrict;
drop schema test_case007 cascade;
create schema test_case007;
drop schema test_case007;
create schema test_case007;
drop schema test_case007 restrict;
create schema test_case007;
drop schema test_case007 cascade;

--tearDown
