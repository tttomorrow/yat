--  @testpoint:opengauss关键字character_set_catalog(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists character_set_catalog;
create group character_set_catalog with password 'gauss@123';
drop group character_set_catalog;

--关键字带双引号-成功
drop group if exists "character_set_catalog";
create group "character_set_catalog" with password 'gauss@123';
drop group "character_set_catalog";

--关键字带单引号-合理报错
drop group if exists 'character_set_catalog';

--关键字带反引号-合理报错
drop group if exists `character_set_catalog`;
