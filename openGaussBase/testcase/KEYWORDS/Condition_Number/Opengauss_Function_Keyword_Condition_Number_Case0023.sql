-- @testpoint: opengauss关键字condition_number(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists condition_number_test;
create table condition_number_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists condition_number;
create index condition_number on condition_number_test(id);
drop index condition_number;

--关键字带双引号-成功
drop index if exists "condition_number";
create index "condition_number" on condition_number_test(id);
drop index "condition_number";

--关键字带单引号-合理报错
drop index if exists 'condition_number';
create index 'condition_number' on condition_number_test(id);

--关键字带反引号-合理报错
drop index if exists `condition_number`;
create index `condition_number` on condition_number_test(id);
drop table if exists condition_number_test;