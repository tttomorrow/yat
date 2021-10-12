-- @testpoint: opengauss关键字defined(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists defined_test;
create table defined_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists defined;
create index defined on defined_test(id);
drop index defined;

--关键字带双引号-成功
drop index if exists "defined";
create index "defined" on defined_test(id);
drop index "defined";

--关键字带单引号-合理报错
drop index if exists 'defined';
create index 'defined' on defined_test(id);

--关键字带反引号-合理报错
drop index if exists `defined`;
create index `defined` on defined_test(id);
drop table if exists defined_test;
