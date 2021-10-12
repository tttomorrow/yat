--  @testpoint:opengauss关键字Inline(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists Inline;
create data source Inline;
drop data source Inline;

--关键字带双引号-成功
drop data source if exists "Inline";
create data source "Inline";
drop data source "Inline";

--关键字带单引号-合理报错
drop data source if exists 'Inline';
create data source 'Inline';

--关键字带反引号-合理报错
drop data source if exists `Inline`;
create data source `Inline`;
