-- @testpoint: opengauss关键字And(保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists And_test;
create table And_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop index if exists And;
create index And on And_test(id);


--关键字带双引号-成功
drop index if exists "And";
create index "And" on And_test(id);

--清理环境
drop index "And";
drop table if exists And_test;
--关键字带单引号-合理报错
drop index if exists 'And';
create index 'And' on And_test(id);

--关键字带反引号-合理报错
drop index if exists `And`;
create index `And` on And_test(id);