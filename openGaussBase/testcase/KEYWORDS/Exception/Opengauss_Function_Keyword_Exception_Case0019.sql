-- @testpoint: opengauss关键字exception(非保留)，作为外部数据源名 合理报错

--关键字不带引号-成功
drop data source if exists exception;
create data source exception;
drop data source exception;

--关键字带双引号-成功
drop data source if exists "exception";
create data source "exception";
drop data source "exception";

--关键字带单引号-合理报错
drop data source if exists 'exception';
create data source 'exception';

--关键字带反引号-合理报错
drop data source if exists `exception`;
create data source `exception`;
