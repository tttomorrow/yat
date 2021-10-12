--  @testpoint:opengauss关键字logging(非保留)，作为角色名


--关键字不带引号-成功
drop role if exists logging;
create role logging with password 'gauss@123' valid until '2020-12-31';
drop role logging;

--关键字带双引号-成功
drop role if exists "logging";
create role "logging" with password 'gauss@123' valid until '2020-12-31';
drop role "logging";

--关键字带单引号-合理报错
drop role if exists 'logging';
create role 'logging' with password 'gauss@123' valid until '2020-12-31';

--关键字带反引号-合理报错
drop role if exists `logging`;
create role `logging` with password 'gauss@123' valid until '2020-12-31';
