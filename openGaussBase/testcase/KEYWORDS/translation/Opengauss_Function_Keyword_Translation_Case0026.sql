--  @testpoint:opengauss关键字translation(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists translation;
create schema translation;
drop schema translation;

--关键字带双引号-成功
drop schema if exists "translation";
create schema "translation";
drop schema "translation";

--关键字带单引号-合理报错
drop schema if exists 'translation';
create schema 'translation';

--关键字带反引号-合理报错
drop schema if exists `translation`;
create schema `translation`;
