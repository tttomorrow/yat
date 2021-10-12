--  @testpoint:opengauss关键字Analyze(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists Analyze;
create schema Analyze;

--关键字带双引号-成功
drop schema if exists "Analyze";
create schema "Analyze";

--清理环境
drop schema "Analyze";

--关键字带单引号-合理报错
drop schema if exists 'Analyze';
create schema 'Analyze';

--关键字带反引号-合理报错
drop schema if exists `Analyze`;
create schema `Analyze`;

