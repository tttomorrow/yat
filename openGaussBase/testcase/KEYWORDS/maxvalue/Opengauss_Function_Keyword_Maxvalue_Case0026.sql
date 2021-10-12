--  @testpoint:opengauss关键字maxvalue(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists maxvalue;
create schema maxvalue;

--关键字带双引号-成功
drop schema if exists "maxvalue";
create schema "maxvalue";

--清理环境
drop schema "maxvalue";

--关键字带单引号-合理报错
drop schema if exists 'maxvalue';
create schema 'maxvalue';

--关键字带反引号-合理报错
drop schema if exists `maxvalue`;
create schema `maxvalue`;

