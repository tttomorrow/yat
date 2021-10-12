--  @testpoint:opengauss关键字checked(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists checked;
create group checked with password 'gauss@123';
drop group checked;

--关键字带双引号-成功
drop group if exists "checked";
create group "checked" with password 'gauss@123';
drop group "checked";

--关键字带单引号-合理报错
drop group if exists 'checked';

--关键字带反引号-合理报错
drop group if exists `checked`;
