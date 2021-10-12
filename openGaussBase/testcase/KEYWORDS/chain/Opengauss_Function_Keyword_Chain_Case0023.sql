-- @testpoint: opengauss关键字chain非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists chain_test;
create table chain_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists chain;
create index chain on chain_test(id);

--清理环境
drop index chain;

--关键字带双引号-成功
drop index if exists "chain";
create index "chain" on chain_test(id);

--清理环境
drop index "chain";

--关键字带单引号-合理报错
drop index if exists 'chain';

--关键字带反引号-合理报错
drop index if exists `chain`;
drop table if exists chain_test;