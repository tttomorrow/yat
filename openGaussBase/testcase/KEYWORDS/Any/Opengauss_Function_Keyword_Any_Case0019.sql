--  @testpoint:opengauss关键字Any(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source Any;

--关键字带双引号-成功
drop data source if exists "Any";
create data source "Any";
drop data source "Any";

--关键字带单引号-合理报错
drop data source if exists 'Any';
create data source 'Any';

--关键字带反引号-合理报错
drop data source if exists `Any`;
create data source `Any`;
