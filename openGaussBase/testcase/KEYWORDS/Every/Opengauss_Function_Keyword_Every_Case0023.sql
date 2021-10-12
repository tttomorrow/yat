-- @testpoint: opengauss关键字every(非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists every_test;
create table every_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists every;
create index every on every_test(id);
drop index every;

--关键字带双引号-成功
drop index if exists "every";
create index "every" on every_test(id);
drop index "every";

--关键字带单引号-合理报错
drop index if exists 'every';
create index 'every' on every_test(id);

--关键字带反引号-合理报错
drop index if exists `every`;
create index `every` on every_test(id);
drop table if exists every_test;