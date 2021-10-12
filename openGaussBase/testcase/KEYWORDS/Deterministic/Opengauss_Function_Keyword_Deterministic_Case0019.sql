--  @testpoint:opengauss关键字deterministic(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists deterministic;
create data source deterministic;
drop data source deterministic;

--关键字带双引号-成功
drop data source if exists "deterministic";
create data source "deterministic";
drop data source "deterministic";

--关键字带单引号-合理报错
drop data source if exists 'deterministic';
create data source 'deterministic';

--关键字带反引号-合理报错
drop data source if exists `deterministic`;
create data source `deterministic`;
