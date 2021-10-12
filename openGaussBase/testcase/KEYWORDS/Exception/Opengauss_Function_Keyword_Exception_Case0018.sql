-- @testpoint: opengauss关键字exception(非保留)，作为数据库名 合理报错

--关键字不带引号-成功
drop database if exists exception;
create database exception;
drop database exception;

--关键字带双引号-成功
drop database if exists "exception";
create database "exception";
drop database "exception";

--关键字带单引号-合理报错
drop database if exists 'exception';
create database 'exception';

--关键字带反引号-合理报错
drop database if exists `exception`;
create database `exception`;

