--  @testpoint:opengauss关键字false(保留)，作为用户组名


--关键字不带引号-失败
drop group if exists false;
create group false with password 'Gauss@123';

--关键字带双引号-成功
drop group if exists "false";
create group "false" with password 'Gauss@123';
drop group "false";

--关键字带单引号-合理报错
drop group if exists 'false';
create group 'false' with password 'Gauss@123';

--关键字带反引号-合理报错
drop group if exists `false`;
create group `false` with password 'Gauss@123';
