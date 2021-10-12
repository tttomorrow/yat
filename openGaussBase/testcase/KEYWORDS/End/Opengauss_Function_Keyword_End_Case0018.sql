--  @testpoint:opengauss关键字end(保留)，作为数据库名

--关键字不带引号-失败
drop database if exists end;
create database end;

--关键字带双引号-成功
drop database if exists "end";
create database "end";
drop database "end";

--关键字带单引号-合理报错
drop database if exists 'end';
create database 'end';

--关键字带反引号-合理报错
drop database if exists `end`;
create database `end`;
