--  @testpoint:opengauss关键字bitvar(非保留)，作为数据库名
--关键字不带引号-成功
drop database if exists bitvar;
create database bitvar;

--清理环境
drop database bitvar;

--关键字带双引号-成功
drop database if exists "bitvar";
create database "bitvar";

--清理环境
drop database "bitvar";

--关键字带单引号-合理报错
drop database if exists 'bitvar';
create database 'bitvar';

--关键字带反引号-合理报错
drop database if exists `bitvar`;
create database `bitvar`;
