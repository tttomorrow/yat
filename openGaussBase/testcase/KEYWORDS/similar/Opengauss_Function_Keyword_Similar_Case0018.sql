-- @testpoint: opengauss关键字similar(保留)，作为数据库名，合理报错

--关键字不带引号-失败
create database similar;

--关键字带双引号-成功
create database "similar";
drop database if exists "similar";

--关键字带单引号-合理报错
create database 'similar';

--关键字带反引号-合理报错
drop database if exists `similar`;
create database `similar`;
