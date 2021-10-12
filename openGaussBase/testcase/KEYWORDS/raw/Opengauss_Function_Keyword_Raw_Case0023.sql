-- @testpoint: opengauss关键字raw非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists raw_test;
create table raw_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists raw;
create index raw on raw_test(id);
drop index raw;

--关键字带双引号-成功
drop index if exists "raw";
create index "raw" on raw_test(id);
drop index "raw";

--关键字带单引号-合理报错
drop index if exists 'raw';


--关键字带反引号-合理报错
drop index if exists `raw`;
--清理环境
drop table if exists raw_test;
