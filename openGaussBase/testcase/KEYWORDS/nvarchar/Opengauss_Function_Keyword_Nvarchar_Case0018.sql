-- @testpoint: opengauss关键字nvarchar(非保留)，作为数据库名 部分测试点合理报错

--step1:关键字不带引号;expect:成功
drop database if exists nvarchar;
create database nvarchar;
drop database nvarchar;

--step2:关键字带双引号;expect:成功
drop database if exists "nvarchar";
create database "nvarchar";
drop database "nvarchar";

--step3:关键字带单引号;expect:合理报错
drop database if exists 'nvarchar';
create database 'nvarchar';

--step4:关键字带反引号;expect:合理报错
drop database if exists `nvarchar`;
create database `nvarchar`;

