-- @testpoint: opengauss关键字similar(保留)，作为模式名，合理报错

--关键字不带引号-合理报错
drop schema if exists similar;
create schema similar;

--关键字带双引号-成功
drop schema if exists "similar";
create schema "similar";

--清理环境
drop schema "similar";

--关键字带单引号-合理报错
drop schema if exists 'similar';
create schema 'similar';

--关键字带反引号-合理报错
drop schema if exists `similar`;
create schema `similar`;

