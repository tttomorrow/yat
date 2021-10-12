--  @testpoint:opengauss关键字log(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists log;
create schema log;
drop schema log;

--关键字带双引号-成功
drop schema if exists "log";
create schema "log";
drop schema "log";

--关键字带单引号-合理报错
drop schema if exists 'log';
create schema 'log';

--关键字带反引号-合理报错
drop schema if exists `log`;
create schema `log`;
