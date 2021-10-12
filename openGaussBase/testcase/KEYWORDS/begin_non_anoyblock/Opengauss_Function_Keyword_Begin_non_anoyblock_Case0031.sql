--  @testpoint:opengauss关键字begin_non_anoyblock(非保留)，作为字段数据类型(合理报错)
--前置条件
drop table if exists begin_non_anoyblock_test cascade;

--关键字不带引号-合理报错
create table begin_non_anoyblock_test(id int,name begin_non_anoyblock);

--关键字带双引号-合理报错
create table begin_non_anoyblock_test(id int,name "begin_non_anoyblock");

--关键字带单引号-合理报错
create table begin_non_anoyblock_test(id int,name 'begin_non_anoyblock');

--关键字带反引号-合理报错
create table begin_non_anoyblock_test(id int,name `begin_non_anoyblock`);
