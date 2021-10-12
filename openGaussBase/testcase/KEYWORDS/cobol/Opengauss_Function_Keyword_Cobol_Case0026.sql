--  @testpoint:opengauss关键字cobol(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists cobol;
create schema cobol;

--清理环境
drop schema cobol;

--关键字带双引号-成功
drop schema if exists "cobol";
create schema "cobol";

--清理环境
drop schema "cobol";

--关键字带单引号-合理报错
drop schema if exists 'cobol';

--关键字带反引号-合理报错
drop schema if exists `cobol`;
