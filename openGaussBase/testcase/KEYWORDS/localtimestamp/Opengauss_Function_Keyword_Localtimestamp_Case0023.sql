-- @testpoint: opengauss关键字localtimestamp(保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists localtimestamp_test;
create table localtimestamp_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists localtimestamp;
create index localtimestamp on localtimestamp_test(id);


--关键字带双引号-成功
drop index if exists "localtimestamp";
create index "localtimestamp" on localtimestamp_test(id);

--清理环境
drop index "localtimestamp";

--关键字带单引号-合理报错
drop index if exists 'localtimestamp';
create index 'localtimestamp' on localtimestamp_test(id);

--关键字带反引号-合理报错
drop index if exists `localtimestamp`;
create index `localtimestamp` on localtimestamp_test(id);
--清理环境
drop table if exists localtimestamp_test cascade;