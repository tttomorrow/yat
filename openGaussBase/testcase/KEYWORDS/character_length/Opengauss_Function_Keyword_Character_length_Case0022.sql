--  @testpoint:opengauss关键字character_length(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists character_length;
create group character_length with password 'gauss@123';
drop group character_length;

--关键字带双引号-成功
drop group if exists "character_length";
create group "character_length" with password 'gauss@123';
drop group "character_length";

--关键字带单引号-合理报错
drop group if exists 'character_length';

--关键字带反引号-合理报错
drop group if exists `character_length`;
