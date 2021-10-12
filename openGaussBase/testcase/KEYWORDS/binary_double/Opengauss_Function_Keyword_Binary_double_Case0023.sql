-- @testpoint: opengauss关键字binary_double非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists binary_double_test;
create table binary_double_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists binary_double;
create index binary_double on binary_double_test(id);

--清理环境
drop index binary_double;

--关键字带双引号-成功
drop index if exists "binary_double";
create index "binary_double" on binary_double_test(id);

--清理环境
drop index "binary_double";

--关键字带单引号-合理报错
drop index if exists 'binary_double';

--关键字带反引号-合理报错
drop index if exists `binary_double`;
drop table if exists binary_double_test;