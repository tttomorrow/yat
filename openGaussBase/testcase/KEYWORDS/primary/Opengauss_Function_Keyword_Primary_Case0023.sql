-- @testpoint: opengauss关键字primary(保留)，作为索引名,合理报错

--前置条件，创建一个表
drop table if exists primary_test;
create table primary_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists primary;
create index primary on primary_test(id);


--关键字带双引号-成功
drop index if exists "primary";
create index "primary" on primary_test(id);

--清理环境
drop index "primary";

--关键字带单引号-合理报错
drop index if exists 'primary';
create index 'primary' on primary_test(id);

--关键字带反引号-合理报错
drop index if exists `primary`;
create index `primary` on primary_test(id);

--清理环境
drop table if exists primary_test;