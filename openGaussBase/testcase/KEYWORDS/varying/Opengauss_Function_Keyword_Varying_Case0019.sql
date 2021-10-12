--  @testpoint:opengauss关键字varying(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists varying;
create data source varying;
drop data source varying;

--关键字带双引号-成功
drop data source if exists "varying";
create data source "varying";
drop data source "varying";

--关键字带单引号-合理报错
drop data source if exists 'varying';
create data source 'varying';

--关键字带反引号-合理报错
drop data source if exists `varying`;
create data source `varying`;
