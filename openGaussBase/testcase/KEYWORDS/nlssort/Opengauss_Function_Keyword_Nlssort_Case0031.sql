--  @testpoint:opengauss关键字nlssort(保留)，作为字段数据类型(合理报错)

--前置条件
drop table if exists nlssort_test cascade;

--关键字不带引号-合理报错
create table nlssort_test(id int,name nlssort);

--关键字带双引号-合理报错
create table nlssort_test(id int,name "nlssort");

--关键字带单引号-合理报错
create table nlssort_test(id int,name 'nlssort');

--关键字带反引号-合理报错
create table nlssort_test(id int,name `nlssort`);