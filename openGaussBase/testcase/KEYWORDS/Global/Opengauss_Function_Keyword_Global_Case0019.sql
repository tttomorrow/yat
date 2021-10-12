--  @testpoint:opengauss关键字Global(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists Global;
create data source Global;
drop data source Global;

--关键字带双引号-成功
drop data source if exists "Global";
create data source "Global";
drop data source "Global";

--关键字带单引号-合理报错
drop data source if exists 'Global';
create data source 'Global';

--关键字带反引号-合理报错
drop data source if exists `Global`;
create data source `Global`;
