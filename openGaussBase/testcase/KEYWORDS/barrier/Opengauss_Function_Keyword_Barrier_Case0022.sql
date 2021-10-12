--  @testpoint:opengauss关键字barrier(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists barrier;
create group barrier with password 'gauss@123';
drop group barrier;

--关键字带双引号-成功
drop group if exists "barrier";
create group "barrier" with password 'gauss@123';
drop group "barrier";

--关键字带单引号-合理报错
drop group if exists 'barrier';

--关键字带反引号-合理报错
drop group if exists `barrier`;
