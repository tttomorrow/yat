--  @testpoint:opengauss关键字deferrable(保留)，作为外部数据源名

--关键字不带引号-失败
drop data source if exists deferrable;
create data source deferrable;

--关键字带双引号-成功
drop data source if exists "deferrable";
create data source "deferrable";
drop data source "deferrable";

--关键字带单引号-合理报错
drop data source if exists 'deferrable';
create data source 'deferrable';

--关键字带反引号-合理报错
drop data source if exists `deferrable`;
create data source `deferrable`;
