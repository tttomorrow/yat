--  @testpoint:opengauss关键字Identity(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists Identity;
create schema Identity;
drop schema Identity;

--关键字带双引号-成功
drop schema if exists "Identity";
create schema "Identity";
drop schema "Identity";

--关键字带单引号-合理报错
drop schema if exists 'Identity';
create schema 'Identity';

--关键字带反引号-合理报错
drop schema if exists `Identity`;
create schema `Identity`;
