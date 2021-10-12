--  @testpoint:opengauss关键字constraint_catalog(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists constraint_catalog;
create schema constraint_catalog;
drop schema constraint_catalog;

--关键字带双引号-成功
drop schema if exists "constraint_catalog";
create schema "constraint_catalog";
drop schema "constraint_catalog";

--关键字带单引号-合理报错
drop schema if exists 'constraint_catalog';
create schema 'constraint_catalog';

--关键字带反引号-合理报错
drop schema if exists `constraint_catalog`;
create schema `constraint_catalog`;
