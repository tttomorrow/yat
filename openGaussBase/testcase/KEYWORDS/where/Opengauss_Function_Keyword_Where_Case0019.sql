--  @testpoint:opengauss关键字where(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source where;

--关键字带双引号-成功
drop data source if exists "where";
create data source "where";
drop data source "where";

--关键字带单引号-合理报错
drop data source if exists 'where';
create data source 'where';

--关键字带反引号-合理报错
drop data source if exists `where`;
create data source `where`;
