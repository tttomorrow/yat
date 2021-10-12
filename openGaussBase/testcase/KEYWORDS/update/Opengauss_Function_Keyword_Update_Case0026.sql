--  @testpoint:opengauss关键字update(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists update;
create schema update;
drop schema update;

--关键字带双引号-成功
drop schema if exists "update";
create schema "update";
drop schema "update";

--关键字带单引号-合理报错
drop schema if exists 'update';
create schema 'update';

--关键字带反引号-合理报错
drop schema if exists `update`;
create schema `update`;
