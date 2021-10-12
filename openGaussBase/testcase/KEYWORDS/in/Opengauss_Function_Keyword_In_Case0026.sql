--  @testpoint:opengauss关键字in(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists in;
create schema in;

--关键字带双引号-成功
drop schema if exists "in";
create schema "in";

--清理环境
drop schema "in";

--关键字带单引号-合理报错
drop schema if exists 'in';
create schema 'in';

--关键字带反引号-合理报错
drop schema if exists `in`;
create schema `in`;

