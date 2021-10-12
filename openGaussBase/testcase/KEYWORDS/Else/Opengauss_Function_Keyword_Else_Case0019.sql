--  @testpoint:opengauss关键字else(保留)，作为外部数据源名

--关键字不带引号-失败
drop data source if exists else;
create data source else;

--关键字带双引号-成功
drop data source if exists "else";
create data source "else";
drop data source "else";

--关键字带单引号-合理报错
drop data source if exists 'else';
create data source 'else';

--关键字带反引号-合理报错
drop data source if exists `else`;
create data source `else`;
