--  @testpoint:opengauss关键字else(保留)，作为数据库名

--关键字不带引号-失败
drop database if exists else;
create database else;

--关键字带双引号-成功
drop database if exists "else";
create database "else";
drop database "else";

--关键字带单引号-合理报错
drop database if exists 'else';
create database 'else';

--关键字带反引号-合理报错
drop database if exists `else`;
create database `else`;
