-- @testpoint: opengauss关键字release非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists release_test;
create table release_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists release;
create index release on release_test(id);
drop index release;

--关键字带双引号-成功
drop index if exists "release";
create index "release" on release_test(id);
drop index "release";

--关键字带单引号-合理报错
drop index if exists 'release';


--关键字带反引号-合理报错
drop index if exists `release`;
drop table if exists release_test;