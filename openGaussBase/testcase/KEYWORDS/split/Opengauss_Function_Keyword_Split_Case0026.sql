--  @testpoint:opengauss关键字split(保留)，作为模式名


--关键字不带引号-成功
drop schema if exists split;
create schema split;

--关键字带双引号-成功
drop schema if exists "split";
create schema "split";
drop schema "split";

--关键字带单引号-合理报错
drop schema if exists 'split';
create schema 'split';

--关键字带反引号-合理报错
drop schema if exists `split`;
create schema `split`;

