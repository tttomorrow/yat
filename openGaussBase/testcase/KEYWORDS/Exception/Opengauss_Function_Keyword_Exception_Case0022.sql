-- @testpoint: opengauss关键字exception(非保留)，作为用户组名 合理报错


--关键字不带引号-成功
drop group if exists exception;
create group exception with password 'gauss@123';
drop group exception;

--关键字带双引号-成功
drop group if exists "exception";
create group "exception" with password 'gauss@123';
drop group "exception";

--关键字带单引号-合理报错
drop group if exists 'exception';
create group 'exception' with password 'gauss@123';

--关键字带反引号-合理报错
drop group if exists `exception`;
create group `exception` with password 'gauss@123';
