--  @testpoint:opengauss关键字do(保留)，作为数据库名

--关键字不带引号-失败
drop database if exists do;
create database do;

--关键字带双引号-成功
drop database if exists "do";
create database "do";
drop database "do";

--关键字带单引号-合理报错
drop database if exists 'do';
create database 'do';

--关键字带反引号-合理报错
drop database if exists `do`;
create database `do`;
