-- @testpoint: opengauss关键字access(非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists access_test;
create table access_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists access;
create index access on access_test(id);

--清理环境
drop index access;

--关键字带双引号-成功
drop index if exists "access";
create index "access" on access_test(id);

--清理环境
drop index "access";
drop table access_test;

--关键字带单引号-合理报错
drop index if exists 'access';

--关键字带反引号-合理报错
drop index if exists `access`;
