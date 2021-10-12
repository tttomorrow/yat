--  @testpoint:opengauss关键字cobol(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists cobol;
create data source cobol;

--清理环境
drop data source cobol;

--关键字带双引号-成功
drop data source if exists "cobol";
create data source "cobol";

--清理环境
drop data source "cobol";

--关键字带单引号-合理报错
drop data source if exists 'cobol';

--关键字带反引号-合理报错
drop data source if exists `cobol`;
