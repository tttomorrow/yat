--  @testpoint:opengauss关键字oids(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists oids;
create schema oids;
drop schema oids;

--关键字带双引号-成功
drop schema if exists "oids";
create schema "oids";
drop schema "oids";

--关键字带单引号-合理报错
drop schema if exists 'oids';
create schema 'oids';

--关键字带反引号-合理报错
drop schema if exists `oids`;
create schema `oids`;
