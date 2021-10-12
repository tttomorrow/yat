--  @testpoint:opengauss关键字decimal(非保留)，作为字段数据类型(合理报错)

--前置条件
drop table if exists decimal_test cascade;

--关键字不带引号-成功
create table decimal_test(id int,name decimal);
drop table decimal_test;

--关键字带双引号-合理报错
create table decimal_test(id int,name "decimal");

--关键字带单引号-合理报错
create table decimal_test(id int,name 'decimal');

--关键字带反引号-合理报错
create table decimal_test(id int,name `decimal`);
