--  @testpoint:opengauss关键字diagnostics(非保留)，作为字段数据类型(合理报错)

--前置条件
drop table if exists diagnostics_test cascade;

--关键字不带引号-合理报错
create table diagnostics_test(id int,name diagnostics);

--关键字带双引号-合理报错
create table diagnostics_test(id int,name "diagnostics");

--关键字带单引号-合理报错
create table diagnostics_test(id int,name 'diagnostics');

--关键字带反引号-合理报错
create table diagnostics_test(id int,name `diagnostics`);
