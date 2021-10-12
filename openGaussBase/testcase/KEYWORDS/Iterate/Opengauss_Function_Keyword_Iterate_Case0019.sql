--  @testpoint:opengauss关键字Iterate(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists Iterate;
create data source Iterate;
drop data source Iterate;

--关键字带双引号-成功
drop data source if exists "Iterate";
create data source "Iterate";
drop data source "Iterate";

--关键字带单引号-合理报错
drop data source if exists 'Iterate';
create data source 'Iterate';

--关键字带反引号-合理报错
drop data source if exists `Iterate`;
create data source `Iterate`;
