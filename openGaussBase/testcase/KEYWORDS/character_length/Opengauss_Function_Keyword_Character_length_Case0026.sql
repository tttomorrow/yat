--  @testpoint:opengauss关键字character_length(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists character_length;
create schema character_length;

--清理环境
drop schema character_length;

--关键字带双引号-成功
drop schema if exists "character_length";
create schema "character_length";

--清理环境
drop schema "character_length";

--关键字带单引号-合理报错
drop schema if exists 'character_length';

--关键字带反引号-合理报错
drop schema if exists `character_length`;
