--  @testpoint:opengauss关键字fetch(保留)，作为数据库名

--关键字不带引号-失败
drop database if exists fetch;
create database fetch;

--关键字带双引号-成功
drop database if exists "fetch";
create database "fetch";
drop database "fetch";

--关键字带单引号-合理报错
drop database if exists 'fetch';
create database 'fetch';

--关键字带反引号-合理报错
drop database if exists `fetch`;
create database `fetch`;
