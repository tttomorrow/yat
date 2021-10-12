-- @testpoint: opengauss关键字limit(保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists limit_test;
create table limit_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists limit;
create index limit on limit_test(id);


--关键字带双引号-成功
drop index if exists "limit";
create index "limit" on limit_test(id);

--清理环境
drop index "limit";

--关键字带单引号-合理报错
drop index if exists 'limit';
create index 'limit' on limit_test(id);

--关键字带反引号-合理报错
drop index if exists `limit`;
create index `limit` on limit_test(id);
--清理环境
drop table if exists limit_test cascade;