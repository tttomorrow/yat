--  @testpoint:opengauss关键字query(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists query;
create data source query;
drop data source query;

--关键字带双引号-成功
drop data source if exists "query";
create data source "query";
drop data source "query";

--关键字带单引号-合理报错
drop data source if exists 'query';

--关键字带反引号-合理报错
drop data source if exists `query`;

