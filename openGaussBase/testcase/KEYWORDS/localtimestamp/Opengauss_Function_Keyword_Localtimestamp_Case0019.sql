--  @testpoint:opengauss关键字localtimestamp(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source localtimestamp;

--关键字带双引号-成功
drop data source if exists "localtimestamp";
create data source "localtimestamp";
drop data source "localtimestamp";

--关键字带单引号-合理报错
drop data source if exists 'localtimestamp';
create data source 'localtimestamp';

--关键字带反引号-合理报错
drop data source if exists `localtimestamp`;
create data source `localtimestamp`;
