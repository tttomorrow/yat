--  @testpoint:opengauss关键字except(保留)，作为数据库名

--关键字不带引号-失败
drop database if exists except;
create database except;

--关键字带双引号-成功
drop database if exists "except";
create database "except";
drop database "except";

--关键字带单引号-合理报错
drop database if exists 'except';
create database 'except';

--关键字带反引号-合理报错
drop database if exists `except`;
create database `except`;
