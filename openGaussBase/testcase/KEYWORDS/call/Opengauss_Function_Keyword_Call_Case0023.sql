-- @testpoint: opengauss关键字call非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists call_test;
create table call_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists call;
create index call on call_test(id);

--清理环境
drop index call;

--关键字带双引号-成功
drop index if exists "call";
create index "call" on call_test(id);

--清理环境
drop index "call";

--关键字带单引号-合理报错
drop index if exists 'call';

--关键字带反引号-合理报错
drop index if exists `call`;
drop table if exists call_test;