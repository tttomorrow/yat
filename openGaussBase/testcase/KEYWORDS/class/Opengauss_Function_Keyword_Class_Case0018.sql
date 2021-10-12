--  @testpoint:opengauss关键字class(非保留)，作为数据库名
--关键字不带引号-成功
drop database if exists class;
create database class;

--清理环境
drop database class;

--关键字带双引号-成功
drop database if exists "class";
create database "class";

--清理环境
drop database "class";

--关键字带单引号-合理报错
drop database if exists 'class';
create database 'class';

--关键字带反引号-合理报错
drop database if exists `class`;
create database `class`;
