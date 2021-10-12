--  @testpoint:opengauss关键字destructor(非保留)，作为数据库名

--关键字不带引号-成功
drop database if exists destructor;
create database destructor;
drop database destructor;

--关键字带双引号-成功
drop database if exists "destructor";
create database "destructor";
drop database "destructor";

--关键字带单引号-合理报错
drop database if exists 'destructor';
create database 'destructor';

--关键字带反引号-合理报错
drop database if exists `destructor`;
create database `destructor`;

