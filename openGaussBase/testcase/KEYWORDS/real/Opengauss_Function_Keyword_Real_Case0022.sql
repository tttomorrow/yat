--  @testpoint:opengauss关键字real(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists real;
create group real with password 'gauss@123';
drop group real;

--关键字带双引号-成功
drop group if exists "real";
create group "real" with password 'gauss@123';
drop group "real";

--关键字带单引号-合理报错
drop group if exists 'real';

--关键字带反引号-合理报错
drop group if exists `real`;

