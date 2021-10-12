--  @testpoint:opengauss关键字server_name(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists server_name;
create schema server_name;
drop schema server_name;

--关键字带双引号-成功
drop schema if exists "server_name";
create schema "server_name";
drop schema "server_name";

--关键字带单引号-合理报错
drop schema if exists 'server_name';
create schema 'server_name';

--关键字带反引号-合理报错
drop schema if exists `server_name`;
create schema `server_name`;
