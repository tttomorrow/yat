--  @testpoint:opengauss关键字checked(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists checked;
create schema checked;

--清理环境
drop schema checked;

--关键字带双引号-成功
drop schema if exists "checked";
create schema "checked";

--清理环境
drop schema "checked";

--关键字带单引号-合理报错
drop schema if exists 'checked';

--关键字带反引号-合理报错
drop schema if exists `checked`;
