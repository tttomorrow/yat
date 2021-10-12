--  @testpoint:opengauss关键字routine_name(非保留)，作为数据库名

--关键字不带引号-成功
drop database if exists routine_name;
create database routine_name;
drop database routine_name;

--关键字带双引号-成功
drop database if exists "routine_name";
create database "routine_name";
drop database "routine_name";

--关键字带单引号-合理报错
drop database if exists 'routine_name';
create database 'routine_name';

--关键字带反引号-合理报错
drop database if exists `routine_name`;
create database `routine_name`;

