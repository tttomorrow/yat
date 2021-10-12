-- @testpoint: opengauss关键字partition非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists partition_test;
create table partition_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists partition;
create index partition on partition_test(id);
drop index partition;

--关键字带双引号-成功
drop index if exists "partition";
create index "partition" on partition_test(id);
drop index "partition";

--关键字带单引号-合理报错
drop index if exists 'partition';
create index 'partition' on partition_test(id);

--关键字带反引号-合理报错
drop index if exists `partition`;
create index `partition` on partition_test(id);
--清理环境
drop table if exists partition_test cascade;
