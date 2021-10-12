--  @testpoint:opengauss关键字using(保留)，作为数据库名

--关键字不带引号-失败
create database using;

--关键字带双引号-成功
create database "using";
drop database if exists "using";

--关键字带单引号-合理报错
create database 'using';

--关键字带反引号-合理报错
drop database if exists `using`;
create database `using`;
