--  @testpoint:opengauss关键字command_function(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists command_function;
create schema command_function;
drop schema command_function;

--关键字带双引号-成功
drop schema if exists "command_function";
create schema "command_function";
drop schema "command_function";

--关键字带单引号-合理报错
drop schema if exists 'command_function';
create schema 'command_function';

--关键字带反引号-合理报错
drop schema if exists `command_function`;
create schema `command_function`;
