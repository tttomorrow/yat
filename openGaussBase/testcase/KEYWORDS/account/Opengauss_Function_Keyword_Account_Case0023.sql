-- @testpoint: opengauss关键字account(非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists account_test;
create table account_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists account;
create index account on account_test(id);

--清理环境
drop index account;

--关键字带双引号-成功
drop index if exists "account";
create index "account" on account_test(id);

--清理环境
drop index "account";

--关键字带单引号-合理报错
drop index if exists 'account';

--关键字带反引号-合理报错
drop index if exists `account`;
drop table if exists account_test;