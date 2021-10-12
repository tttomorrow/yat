--  @testpoint:opengauss关键字Any(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists Any;
create schema Any;

--关键字带双引号-成功
drop schema if exists "Any";
create schema "Any";

--清理环境
drop schema "Any";

--关键字带单引号-合理报错
drop schema if exists 'Any';
create schema 'Any';

--关键字带反引号-合理报错
drop schema if exists `Any`;
create schema `Any`;

