--  @testpoint:opengauss关键字column_name(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists column_name;
create data source column_name;
drop data source column_name;

--关键字带双引号-成功
drop data source if exists "column_name";
create data source "column_name";
drop data source "column_name";

--关键字带单引号-合理报错
drop data source if exists 'column_name';
create data source 'column_name';

--关键字带反引号-合理报错
drop data source if exists `column_name`;
create data source `column_name`;
