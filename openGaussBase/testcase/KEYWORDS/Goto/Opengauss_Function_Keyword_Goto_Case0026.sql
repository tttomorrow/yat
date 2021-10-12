--  @testpoint:opengauss关键字Goto(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists Goto;
create schema Goto;
drop schema Goto;

--关键字带双引号-成功
drop schema if exists "Goto";
create schema "Goto";
drop schema "Goto";

--关键字带单引号-合理报错
drop schema if exists 'Goto';
create schema 'Goto';

--关键字带反引号-合理报错
drop schema if exists `Goto`;
create schema `Goto`;
