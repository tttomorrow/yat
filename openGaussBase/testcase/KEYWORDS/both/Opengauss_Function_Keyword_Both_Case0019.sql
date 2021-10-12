--  @testpoint:opengauss关键字Both(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source Both;

--关键字带双引号-成功
drop data source if exists "Both";
create data source "Both";
drop data source "Both";

--关键字带单引号-合理报错
drop data source if exists 'Both';
create data source 'Both';

--关键字带反引号-合理报错
drop data source if exists `Both`;
create data source `Both`;
