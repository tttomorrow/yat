-- @testpoint: opengauss关键字verbose(保留)，作为外部数据源名 合理报错

--关键字不带引号-合理报错
create data source verbose;

--关键字带双引号-成功
drop data source if exists "verbose";
create data source "verbose";
drop data source "verbose";

--关键字带单引号-合理报错
drop data source if exists 'verbose';
create data source 'verbose';

--关键字带反引号-合理报错
drop data source if exists `verbose`;
create data source `verbose`;
