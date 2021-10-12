--  @testpoint:opengauss关键字datetime_interval_code(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists datetime_interval_code;
create group datetime_interval_code with password 'gauss@123';
drop group datetime_interval_code;

--关键字带双引号-成功
drop group if exists "datetime_interval_code";
create group "datetime_interval_code" with password 'gauss@123';
drop group "datetime_interval_code";

--关键字带单引号-合理报错
drop group if exists 'datetime_interval_code';
create group 'datetime_interval_code' with password 'gauss@123';

--关键字带反引号-合理报错
drop group if exists `datetime_interval_code`;
create group `datetime_interval_code` with password 'gauss@123';
