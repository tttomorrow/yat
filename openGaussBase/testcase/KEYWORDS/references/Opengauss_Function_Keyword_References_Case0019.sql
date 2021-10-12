--  @testpoint:opengauss关键字references(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source references;

--关键字带双引号-成功
drop data source if exists "references";
create data source "references";
drop data source "references";

--关键字带单引号-合理报错
drop data source if exists 'references';
create data source 'references';

--关键字带反引号-合理报错
drop data source if exists `references`;
create data source `references`;
