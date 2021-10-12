--  @testpoint:opengauss关键字real(非保留)，作为数据库名

--关键字不带引号-成功
drop database if exists real;
create database real;
drop database real;

--关键字带双引号-成功
drop database if exists "real";
create database "real";
drop database "real";

--关键字带单引号-合理报错
drop database if exists 'real';
create database 'real';

--关键字带反引号-合理报错
drop database if exists `real`;
create database `real`;

