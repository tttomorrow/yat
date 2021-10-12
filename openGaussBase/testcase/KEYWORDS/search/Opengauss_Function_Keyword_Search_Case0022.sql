--  @testpoint:opengauss关键字search(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists search;
create group search with password 'Gauss@123';
drop group search;

--关键字带双引号-成功
drop group if exists "search";
create group "search" with password 'Gauss@123';
drop group "search";

--关键字带单引号-合理报错
drop group if exists 'search';
create group 'search' with password 'Gauss@123';

--关键字带反引号-合理报错
drop group if exists `search`;
create group `search` with password 'Gauss@123';
