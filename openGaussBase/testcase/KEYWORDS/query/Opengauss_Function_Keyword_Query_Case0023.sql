-- @testpoint: opengauss关键字query非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists query_test;
create table query_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists query;
create index query on query_test(id);
drop index query;

--关键字带双引号-成功
drop index if exists "query";
create index "query" on query_test(id);
drop index "query";

--关键字带单引号-合理报错
drop index if exists 'query';


--关键字带反引号-合理报错
drop index if exists `query`;
--清理环境
drop table if exists query_test;
