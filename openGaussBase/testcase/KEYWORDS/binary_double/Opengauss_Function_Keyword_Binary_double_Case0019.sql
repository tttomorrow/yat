--  @testpoint:opengauss关键字binary_double(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists binary_double;
create data source binary_double;

--清理环境
drop data source binary_double;

--关键字带双引号-成功
drop data source if exists "binary_double";
create data source "binary_double";

--清理环境
drop data source "binary_double";

--关键字带单引号-合理报错
drop data source if exists 'binary_double';

--关键字带反引号-合理报错
drop data source if exists `binary_double`;
