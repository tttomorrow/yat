--  @testpoint:opengauss关键字absolute(非保留)，作为字段数据类型(合理报错)
--前置条件
drop table if exists absolute_test cascade;

--关键字不带引号-合理报错
create table absolute_test(id int,name absolute);

--关键字带双引号-合理报错
create table absolute_test(id int,name "absolute");

--关键字带单引号-合理报错
create table absolute_test(id int,name 'absolute');

--关键字带反引号-合理报错
create table absolute_test(id int,name `absolute`);
