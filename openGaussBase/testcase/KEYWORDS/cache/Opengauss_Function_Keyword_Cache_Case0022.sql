--  @testpoint:opengauss关键字cache(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists cache;
create group cache with password 'gauss@123';
drop group cache;

--关键字带双引号-成功
drop group if exists "cache";
create group "cache" with password 'gauss@123';
drop group "cache";

--关键字带单引号-合理报错
drop group if exists 'cache';

--关键字带反引号-合理报错
drop group if exists `cache`;
