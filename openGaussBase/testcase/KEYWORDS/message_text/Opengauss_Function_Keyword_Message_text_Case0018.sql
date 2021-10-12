--  @testpoint:opengauss关键字message_text(非保留)，作为数据库名

--关键字不带引号-成功
drop database if exists message_text;
create database message_text;
drop database message_text;

--关键字带双引号-成功
drop database if exists "message_text";
create database "message_text";
drop database "message_text";

--关键字带单引号-合理报错
drop database if exists 'message_text';
create database 'message_text';

--关键字带反引号-合理报错
drop database if exists `message_text`;
create database `message_text`;

