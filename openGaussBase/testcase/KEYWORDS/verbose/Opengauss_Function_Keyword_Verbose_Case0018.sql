-- @testpoint: opengauss关键字verbose(保留)，作为数据库名 合理报错

--关键字不带引号-失败
create database verbose;

--关键字带双引号-成功
create database "verbose";
drop database if exists "verbose";

--关键字带单引号-合理报错
create database 'verbose';

--关键字带反引号-合理报错
drop database if exists `verbose`;
create database `verbose`;
