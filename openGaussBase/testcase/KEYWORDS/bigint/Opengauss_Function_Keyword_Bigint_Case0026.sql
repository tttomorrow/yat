--  @testpoint:opengauss关键字bigint(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists bigint;
create schema bigint;

--清理环境
drop schema bigint;

--关键字带双引号-成功
drop schema if exists "bigint";
create schema "bigint";

--清理环境
drop schema "bigint";

--关键字带单引号-合理报错
drop schema if exists 'bigint';

--关键字带反引号-合理报错
drop schema if exists `bigint`;
