-- @testpoint: opengauss关键字preserve非保留)，作为索引名,合理报错

--前置条件，创建一个表
drop table if exists preserve_test;
create table preserve_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists preserve;
create index preserve on preserve_test(id);
drop index preserve;

--关键字带双引号-成功
drop index if exists "preserve";
create index "preserve" on preserve_test(id);
drop index "preserve";

--关键字带单引号-合理报错
drop index if exists 'preserve';
create index 'preserve' on preserve_test(id);

--关键字带反引号-合理报错
drop index if exists `preserve`;
create index `preserve` on preserve_test(id);

--清理环境
drop table if exists preserve_test;