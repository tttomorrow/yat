--  @testpoint:opengauss关键字Location(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists Location;
create group Location with password 'Gauss@123';
drop group Location;

--关键字带双引号-成功
drop group if exists "Location";
create group "Location" with password 'Gauss@123';
drop group "Location";

--关键字带单引号-合理报错
drop group if exists 'Location';
create group 'Location' with password 'Gauss@123';

--关键字带反引号-合理报错
drop group if exists `Location`;
create group `Location` with password 'Gauss@123';
