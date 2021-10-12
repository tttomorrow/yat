--  @testpoint:opengauss关键字overriding(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists overriding;
create data source overriding;
drop data source overriding;

--关键字带双引号-成功
drop data source if exists "overriding";
create data source "overriding";
drop data source "overriding";

--关键字带单引号-合理报错
drop data source if exists 'overriding';
create data source 'overriding';

--关键字带反引号-合理报错
drop data source if exists `overriding`;
create data source `overriding`;
