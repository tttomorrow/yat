-- @testpoint: opengauss关键字discard(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists discard_test;
create table discard_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists discard;
create index discard on discard_test(id);
drop index discard;

--关键字带双引号-成功
drop index if exists "discard";
create index "discard" on discard_test(id);
drop index "discard";

--关键字带单引号-合理报错
drop index if exists 'discard';
create index 'discard' on discard_test(id);

--关键字带反引号-合理报错
drop index if exists `discard`;
create index `discard` on discard_test(id);
drop table if exists discard_test;
