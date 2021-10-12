--  @testpoint:opengauss关键字nchar(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists nchar;
create schema nchar;
drop schema nchar;

--关键字带双引号-成功
drop schema if exists "nchar";
create schema "nchar";
drop schema "nchar";

--关键字带单引号-合理报错
drop schema if exists 'nchar';
create schema 'nchar';

--关键字带反引号-合理报错
drop schema if exists `nchar`;
create schema `nchar`;
