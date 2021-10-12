-- @testpoint: opengauss关键字contains(非保留)，作为用户组名，部分测试点合理报错


--关键字不带引号-成功
drop group if exists contains;
create group contains with password 'gauss@123';
drop group if exists contains;

--关键字带双引号-成功
drop group if exists "contains";
create group "contains" with password 'gauss@123';
drop group if exists "contains";

--关键字带单引号-合理报错
drop group if exists 'contains';
create group 'contains' with password 'gauss@123';

--关键字带反引号-合理报错
drop group if exists `contains`;
create group `contains` with password 'gauss@123';
