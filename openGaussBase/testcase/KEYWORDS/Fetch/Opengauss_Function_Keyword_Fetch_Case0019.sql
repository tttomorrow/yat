--  @testpoint:opengauss关键字fetch(保留)，作为外部数据源名

--关键字不带引号-失败
drop data source if exists fetch;
create data source fetch;

--关键字带双引号-成功
drop data source if exists "fetch";
create data source "fetch";
drop data source "fetch";

--关键字带单引号-合理报错
drop data source if exists 'fetch';
create data source 'fetch';

--关键字带反引号-合理报错
drop data source if exists `fetch`;
create data source `fetch`;
