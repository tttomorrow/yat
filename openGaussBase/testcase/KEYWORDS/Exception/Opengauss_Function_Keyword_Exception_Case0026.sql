-- @testpoint: opengauss关键字exception(非保留)，作为模式名 合理报错


--关键字不带引号-成功
drop schema if exists exception;
create schema exception;
drop schema exception;

--关键字带双引号-成功
drop schema if exists "exception";
create schema "exception";
drop schema "exception";

--关键字带单引号-合理报错
drop schema if exists 'exception';
create schema 'exception';

--关键字带反引号-合理报错
drop schema if exists `exception`;
create schema `exception`;
