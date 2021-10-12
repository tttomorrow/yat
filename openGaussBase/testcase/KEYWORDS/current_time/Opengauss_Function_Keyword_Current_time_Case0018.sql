--  @testpoint:opengauss关键字current_time(保留)，作为数据库名

--关键字不带引号-失败
create database current_time;

--关键字带双引号-成功
create database "current_time";
drop database if exists "current_time";

--关键字带单引号-合理报错
create database 'current_time';

--关键字带反引号-合理报错
drop database if exists `current_time`;
create database `current_time`;
