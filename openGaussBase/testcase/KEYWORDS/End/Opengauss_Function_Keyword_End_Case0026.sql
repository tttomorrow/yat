--  @testpoint:opengauss关键字end(保留)，作为模式名


--关键字不带引号-失败
drop schema if exists end;
create schema end;

--关键字带双引号-成功
drop schema if exists "end";
create schema "end";
drop schema "end";

--关键字带单引号-合理报错
drop schema if exists 'end';
create schema 'end';

--关键字带反引号-合理报错
drop schema if exists `end`;
create schema `end`;

