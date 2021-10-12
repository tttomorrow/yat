--  @testpoint:opengauss关键字returns(非保留)，作为用户组名
--关键字不带引号-成功
drop group if exists returns;
create group returns with password 'gauss@123';
drop group returns;

--关键字带双引号-成功
drop group if exists "returns";
create group "returns" with password 'gauss@123';
drop group "returns";

--关键字带单引号-合理报错
drop group if exists 'returns';

--关键字带反引号-合理报错
drop group if exists `returns`;
