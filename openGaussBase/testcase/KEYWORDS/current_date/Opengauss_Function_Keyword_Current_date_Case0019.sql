--  @testpoint:opengauss关键字current_date(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source current_date;

--关键字带双引号-成功
drop data source if exists "current_date";
create data source "current_date";
drop data source "current_date";

--关键字带单引号-合理报错
drop data source if exists 'current_date';
create data source 'current_date';

--关键字带反引号-合理报错
drop data source if exists `current_date`;
create data source `current_date`;
