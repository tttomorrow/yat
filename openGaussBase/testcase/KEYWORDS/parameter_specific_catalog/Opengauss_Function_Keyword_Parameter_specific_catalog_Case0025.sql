--  @testpoint:opengauss关键字parameter_specific_catalog(非保留)，作为角色名


--关键字不带引号-成功
drop role if exists parameter_specific_catalog;
create role parameter_specific_catalog with password 'gauss@123' valid until '2020-12-31';
drop role parameter_specific_catalog;

--关键字带双引号-成功
drop role if exists "parameter_specific_catalog";
create role "parameter_specific_catalog" with password 'gauss@123' valid until '2020-12-31';
drop role "parameter_specific_catalog";

--关键字带单引号-合理报错
drop role if exists 'parameter_specific_catalog';
create role 'parameter_specific_catalog' with password 'gauss@123' valid until '2020-12-31';

--关键字带反引号-合理报错
drop role if exists `parameter_specific_catalog`;
create role `parameter_specific_catalog` with password 'gauss@123' valid until '2020-12-31';
