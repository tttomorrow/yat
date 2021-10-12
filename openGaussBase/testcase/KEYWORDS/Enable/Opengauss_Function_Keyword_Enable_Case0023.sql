-- @testpoint: opengauss关键字enable(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists enable_test;
create table enable_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists enable;
create index enable on enable_test(id);
drop index enable;

--关键字带双引号-成功
drop index if exists "enable";
create index "enable" on enable_test(id);
drop index "enable";

--关键字带单引号-合理报错
drop index if exists 'enable';
create index 'enable' on enable_test(id);

--关键字带反引号-合理报错
drop index if exists `enable`;
create index `enable` on enable_test(id);
drop table if exists enable_test;
