--  @testpoint:opengauss关键字into(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists into;
create schema into;

--关键字带双引号-成功
drop schema if exists "into";
create schema "into";

--清理环境
drop schema "into";

--关键字带单引号-合理报错
drop schema if exists 'into';
create schema 'into';

--关键字带反引号-合理报错
drop schema if exists `into`;
create schema `into`;

