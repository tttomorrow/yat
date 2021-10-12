--  @testpoint:opengauss关键字revoke(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists revoke;
create data source revoke;

--清理环境
drop data source revoke;

--关键字带双引号-成功
drop data source if exists "revoke";
create data source "revoke";

--清理环境
drop data source "revoke";

--关键字带单引号-合理报错
drop data source if exists 'revoke';

--关键字带反引号-合理报错
drop data source if exists `revoke`;
