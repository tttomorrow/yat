--  @testpoint:opengauss关键字Check(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists Check;
create schema Check;

--关键字带双引号-成功
drop schema if exists "Check";
create schema "Check";

--清理环境
drop schema "Check";

--关键字带单引号-合理报错
drop schema if exists 'Check';
create schema 'Check';

--关键字带反引号-合理报错
drop schema if exists `Check`;
create schema `Check`;

