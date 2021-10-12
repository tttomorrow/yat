-- @testpoint: opengauss关键字privilege非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists privilege_test;
create table privilege_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists privilege;
create index privilege on privilege_test(id);
drop index privilege;

--关键字带双引号-成功
drop index if exists "privilege";
create index "privilege" on privilege_test(id);
drop index "privilege";

--关键字带单引号-合理报错
drop index if exists 'privilege';


--关键字带反引号-合理报错
drop index if exists `privilege`;

--清理环境
drop table if exists privilege_test;