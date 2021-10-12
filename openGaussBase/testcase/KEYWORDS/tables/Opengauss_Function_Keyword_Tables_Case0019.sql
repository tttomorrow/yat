--  @testpoint:opengauss关键字tables(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists tables;
create data source tables;
drop data source tables;

--关键字带双引号-成功
drop data source if exists "tables";
create data source "tables";
drop data source "tables";

--关键字带单引号-合理报错
drop data source if exists 'tables';
create data source 'tables';

--关键字带反引号-合理报错
drop data source if exists `tables`;
create data source `tables`;
