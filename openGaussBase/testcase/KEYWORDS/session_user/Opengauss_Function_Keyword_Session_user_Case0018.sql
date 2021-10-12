--  @testpoint:opengauss关键字session_user(保留)，作为数据库名

--关键字不带引号-失败
create database session_user;

--关键字带双引号-成功
create database "session_user";
drop database if exists "session_user";

--关键字带单引号-合理报错
create database 'session_user';

--关键字带反引号-合理报错
drop database if exists `session_user`;
create database `session_user`;
