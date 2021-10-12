--  @testpoint:opengauss关键字public(非保留)，作为用户组名


--关键字不带引号-合理报错
drop group if exists public;
create group public with password 'gauss@123';
drop group public;

--关键字带双引号-合理报错
drop group if exists "public";
create group "public" with password 'gauss@123';

--关键字带单引号-合理报错
drop group if exists 'public';

--关键字带反引号-合理报错
drop group if exists `public`;

