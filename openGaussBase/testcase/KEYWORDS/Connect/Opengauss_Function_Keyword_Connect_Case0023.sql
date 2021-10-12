-- @testpoint: opengauss关键字connect(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists connect_test;
create table connect_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists connect;
create index connect on connect_test(id);
drop index connect;

--关键字带双引号-成功
drop index if exists "connect";
create index "connect" on connect_test(id);
drop index "connect";

--关键字带单引号-合理报错
drop index if exists 'connect';
create index 'connect' on connect_test(id);

--关键字带反引号-合理报错
drop index if exists `connect`;
create index `connect` on connect_test(id);
drop table if exists connect_test;