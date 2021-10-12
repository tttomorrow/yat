--  @testpoint:opengauss关键字parameter_specific_name(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists parameter_specific_name;
create schema parameter_specific_name;
drop schema parameter_specific_name;

--关键字带双引号-成功
drop schema if exists "parameter_specific_name";
create schema "parameter_specific_name";
drop schema "parameter_specific_name";

--关键字带单引号-合理报错
drop schema if exists 'parameter_specific_name';
create schema 'parameter_specific_name';

--关键字带反引号-合理报错
drop schema if exists `parameter_specific_name`;
create schema `parameter_specific_name`;
