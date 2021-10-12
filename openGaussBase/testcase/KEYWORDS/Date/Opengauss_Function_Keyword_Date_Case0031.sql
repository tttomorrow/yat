--  @testpoint:opengauss关键字date(非保留)，作为字段数据类型

--前置条件
drop table if exists date_test cascade;

--关键字不带引号-创建成功
create table date_test(id int,name date);
drop table date_test;

--关键字带双引号-创建成功
create table date_test(id int,name "date");
drop table date_test;

--关键字带单引号-合理报错
create table date_test(id int,name 'date');

--关键字带反引号-合理报错
create table date_test(id int,name `date`);
