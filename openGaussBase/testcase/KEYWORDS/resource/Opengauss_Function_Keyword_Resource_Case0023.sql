-- @testpoint: opengauss关键字resource非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists resource_test;
create table resource_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists resource;
create index resource on resource_test(id);
drop index resource;

--关键字带双引号-成功
drop index if exists "resource";
create index "resource" on resource_test(id);
drop index "resource";

--关键字带单引号-合理报错
drop index if exists 'resource';


--关键字带反引号-合理报错
drop index if exists `resource`;
drop table if exists resource_test;
