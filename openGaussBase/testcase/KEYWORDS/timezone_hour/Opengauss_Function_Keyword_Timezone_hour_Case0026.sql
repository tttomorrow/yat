--  @testpoint:opengauss关键字timezone_hour(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists timezone_hour;
create schema timezone_hour;
drop schema timezone_hour;

--关键字带双引号-成功
drop schema if exists "timezone_hour";
create schema "timezone_hour";
drop schema "timezone_hour";

--关键字带单引号-合理报错
drop schema if exists 'timezone_hour';
create schema 'timezone_hour';

--关键字带反引号-合理报错
drop schema if exists `timezone_hour`;
create schema `timezone_hour`;
