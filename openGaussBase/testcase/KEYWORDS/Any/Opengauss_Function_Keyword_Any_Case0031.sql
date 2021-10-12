--  @testpoint:opengauss关键字Any(保留)，作为字段数据类型(合理报错)

--前置条件
drop table if exists Any_test cascade;

--关键字不带引号-合理报错
create table Any_test(id int,name Any);

--关键字带双引号-合理报错
create table Any_test(id int,name "Any");

--关键字带单引号-合理报错
create table Any_test(id int,name 'Any');

--关键字带反引号-合理报错
create table Any_test(id int,name `Any`);