--  @testpoint:opengauss关键字Asc(保留)，作为数据库名

--关键字不带引号-失败
create database Asc;

--关键字带双引号-成功
create database "Asc";
drop database if exists "Asc";

--关键字带单引号-合理报错
create database 'Asc';

--关键字带反引号-合理报错
drop database if exists `Asc`;
create database `Asc`;
