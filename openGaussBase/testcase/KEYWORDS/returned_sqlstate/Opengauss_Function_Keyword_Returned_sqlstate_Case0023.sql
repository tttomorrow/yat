-- @testpoint: opengauss关键字returned_sqlstate非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists returned_sqlstate_test;
create table returned_sqlstate_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists returned_sqlstate;
create index returned_sqlstate on returned_sqlstate_test(id);

--清理环境
drop index returned_sqlstate;

--关键字带双引号-成功
drop index if exists "returned_sqlstate";
create index "returned_sqlstate" on returned_sqlstate_test(id);

--清理环境
drop index "returned_sqlstate";

--关键字带单引号-合理报错
drop index if exists 'returned_sqlstate';

--关键字带反引号-合理报错
drop index if exists `returned_sqlstate`;
drop table if exists returned_sqlstate_test;