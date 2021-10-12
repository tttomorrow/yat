-- @testpoint: opengauss关键字range非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists range_test;
create table range_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists range;
create index range on range_test(id);
drop index range;

--关键字带双引号-成功
drop index if exists "range";
create index "range" on range_test(id);
drop index "range";

--关键字带单引号-合理报错
drop index if exists 'range';


--关键字带反引号-合理报错
drop index if exists `range`;

--清理环境
drop table if exists range_test;