-- @testpoint: opengauss关键字like(保留)，作为模式名 合理报错

--关键字不带引号-合理报错
drop schema if exists like;
create schema like;

--关键字带双引号-成功
drop schema if exists "like";
create schema "like";

--清理环境
drop schema "like";

--关键字带单引号-合理报错
drop schema if exists 'like';
create schema 'like';

--关键字带反引号-合理报错
drop schema if exists `like`;
create schema `like`;

