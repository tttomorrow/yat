--  @testpoint:opengauss关键字then(保留)，作为模式名


--关键字不带引号-失败
drop schema if exists then;
create schema then;

--关键字带双引号-成功
drop schema if exists "then";
create schema "then";
drop schema "then";

--关键字带单引号-合理报错
drop schema if exists 'then';
create schema 'then';

--关键字带反引号-合理报错
drop schema if exists `then`;
create schema `then`;

