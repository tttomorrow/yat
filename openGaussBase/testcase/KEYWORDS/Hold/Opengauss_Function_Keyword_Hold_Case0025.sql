--  @testpoint:opengauss关键字Hold(非保留)，作为角色名


--关键字不带引号-成功
drop role if exists Hold;
create role Hold with password 'gauss@123' valid until '2020-12-31';
drop role Hold;

--关键字带双引号-成功
drop role if exists "Hold";
create role "Hold" with password 'gauss@123' valid until '2020-12-31';
drop role "Hold";

--关键字带单引号-合理报错
drop role if exists 'Hold';
create role 'Hold' with password 'gauss@123' valid until '2020-12-31';

--关键字带反引号-合理报错
drop role if exists `Hold`;
create role `Hold` with password 'gauss@123' valid until '2020-12-31';
