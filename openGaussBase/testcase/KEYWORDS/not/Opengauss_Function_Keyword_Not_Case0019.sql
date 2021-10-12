--  @testpoint:opengauss关键字not(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source not;

--关键字带双引号-成功
drop data source if exists "not";
create data source "not";
drop data source "not";

--关键字带单引号-合理报错
drop data source if exists 'not';
create data source 'not';

--关键字带反引号-合理报错
drop data source if exists `not`;
create data source `not`;
