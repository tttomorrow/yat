-- @testpoint: opengauss关键字repeatable非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists repeatable_test;
create table repeatable_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists repeatable;
create index repeatable on repeatable_test(id);
drop index repeatable;

--关键字带双引号-成功
drop index if exists "repeatable";
create index "repeatable" on repeatable_test(id);
drop index "repeatable";

--关键字带单引号-合理报错
drop index if exists 'repeatable';


--关键字带反引号-合理报错
drop index if exists `repeatable`;
drop table if exists repeatable_test;
