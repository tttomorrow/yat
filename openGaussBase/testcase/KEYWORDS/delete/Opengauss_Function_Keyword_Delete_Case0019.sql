--  @testpoint:opengauss关键字delete(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists delete;
create data source delete;
drop data source delete;

--关键字带双引号-成功
drop data source if exists "delete";
create data source "delete";
drop data source "delete";

--关键字带单引号-合理报错
drop data source if exists 'delete';
create data source 'delete';

--关键字带反引号-合理报错
drop data source if exists `delete`;
create data source `delete`;
