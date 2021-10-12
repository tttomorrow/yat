--  @testpoint:opengauss关键字unusable(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists unusable;
create data source unusable;
drop data source unusable;

--关键字带双引号-成功
drop data source if exists "unusable";
create data source "unusable";
drop data source "unusable";

--关键字带单引号-合理报错
drop data source if exists 'unusable';
create data source 'unusable';

--关键字带反引号-合理报错
drop data source if exists `unusable`;
create data source `unusable`;
