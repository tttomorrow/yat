--  @testpoint:opengauss关键字character_set_catalog(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists character_set_catalog;
create data source character_set_catalog;

--清理环境
drop data source character_set_catalog;

--关键字带双引号-成功
drop data source if exists "character_set_catalog";
create data source "character_set_catalog";

--清理环境
drop data source "character_set_catalog";

--关键字带单引号-合理报错
drop data source if exists 'character_set_catalog';

--关键字带反引号-合理报错
drop data source if exists `character_set_catalog`;
