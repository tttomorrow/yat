--  @testpoint:opengauss关键字without(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists without;
create data source without;
drop data source without;

--关键字带双引号-成功
drop data source if exists "without";
create data source "without";
drop data source "without";

--关键字带单引号-合理报错
drop data source if exists 'without';
create data source 'without';

--关键字带反引号-合理报错
drop data source if exists `without`;
create data source `without`;
