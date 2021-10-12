-- @testpoint: opengauss关键字privileges非保留)，作为索引名,部分测试点合理报错

--前置条件，创建一个表
drop table if exists privileges_test;
create table privileges_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists privileges;
create index privileges on privileges_test(id);
drop index privileges;

--关键字带双引号-成功
drop index if exists "privileges";
create index "privileges" on privileges_test(id);
drop index "privileges";

--关键字带单引号-合理报错
drop index if exists 'privileges';


--关键字带反引号-合理报错
drop index if exists `privileges`;

--清理环境
drop table if exists privileges_test;