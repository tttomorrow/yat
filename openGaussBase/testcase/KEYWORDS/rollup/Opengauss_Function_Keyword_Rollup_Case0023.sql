-- @testpoint: opengauss关键字rollup非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists rollup_test;
create table rollup_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists rollup;
create index rollup on rollup_test(id);

--清理环境
drop index rollup;

--关键字带双引号-成功
drop index if exists "rollup";
create index "rollup" on rollup_test(id);

--清理环境
drop index "rollup";

--关键字带单引号-合理报错
drop index if exists 'rollup';

--关键字带反引号-合理报错
drop index if exists `rollup`;
drop table if exists rollup_test;