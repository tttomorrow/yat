--  @testpoint:opengauss关键字dec(非保留)，作为字段数据类型

--前置条件
drop table if exists dec_test cascade;

--关键字不带引号-成功
create table dec_test(id int,name dec);
drop table dec_test;

--关键字带双引号-合理报错
create table dec_test(id int,name "dec");

--关键字带单引号-合理报错
create table dec_test(id int,name 'dec');

--关键字带反引号-合理报错
create table dec_test(id int,name `dec`);
