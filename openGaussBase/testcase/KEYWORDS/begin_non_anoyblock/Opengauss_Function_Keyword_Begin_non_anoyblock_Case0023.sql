-- @testpoint: opengauss关键字begin_non_anoyblock非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists begin_non_anoyblock_test;
create table begin_non_anoyblock_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists begin_non_anoyblock;
create index begin_non_anoyblock on begin_non_anoyblock_test(id);

--清理环境
drop index begin_non_anoyblock;

--关键字带双引号-成功
drop index if exists "begin_non_anoyblock";
create index "begin_non_anoyblock" on begin_non_anoyblock_test(id);

--清理环境
drop index "begin_non_anoyblock";

--关键字带单引号-合理报错
drop index if exists 'begin_non_anoyblock';

--关键字带反引号-合理报错
drop index if exists `begin_non_anoyblock`;
drop table if exists begin_non_anoyblock_test;