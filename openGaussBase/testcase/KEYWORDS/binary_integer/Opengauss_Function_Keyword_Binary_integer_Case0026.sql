--  @testpoint:opengauss关键字binary_integer(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists binary_integer;
create schema binary_integer;

--清理环境
drop schema binary_integer;

--关键字带双引号-成功
drop schema if exists "binary_integer";
create schema "binary_integer";

--清理环境
drop schema "binary_integer";

--关键字带单引号-合理报错
drop schema if exists 'binary_integer';

--关键字带反引号-合理报错
drop schema if exists `binary_integer`;
