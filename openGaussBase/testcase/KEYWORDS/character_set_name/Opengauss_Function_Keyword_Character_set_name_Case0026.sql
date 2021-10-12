--  @testpoint:opengauss关键字character_set_name(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists character_set_name;
create schema character_set_name;

--清理环境
drop schema character_set_name;

--关键字带双引号-成功
drop schema if exists "character_set_name";
create schema "character_set_name";

--清理环境
drop schema "character_set_name";

--关键字带单引号-合理报错
drop schema if exists 'character_set_name';

--关键字带反引号-合理报错
drop schema if exists `character_set_name`;
