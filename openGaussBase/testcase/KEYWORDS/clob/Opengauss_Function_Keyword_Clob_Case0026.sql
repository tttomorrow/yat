--  @testpoint:opengauss关键字clob(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists clob;
create schema clob;

--清理环境
drop schema clob;

--关键字带双引号-成功
drop schema if exists "clob";
create schema "clob";

--清理环境
drop schema "clob";

--关键字带单引号-合理报错
drop schema if exists 'clob';

--关键字带反引号-合理报错
drop schema if exists `clob`;
