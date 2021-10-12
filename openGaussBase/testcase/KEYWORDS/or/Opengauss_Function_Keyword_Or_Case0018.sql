--  @testpoint:opengauss关键字or(保留)，作为数据库名

--关键字不带引号-失败
create database or;

--关键字带双引号-成功
create database "or";
drop database if exists "or";

--关键字带单引号-合理报错
create database 'or';

--关键字带反引号-合理报错
drop database if exists `or`;
create database `or`;
