-- @testpoint: opengauss关键字collation_schema(非保留)，作为模式名 合理报错


--关键字不带引号-成功
drop schema if exists collation_schema;
create schema collation_schema;
drop schema collation_schema;

--关键字带双引号-成功
drop schema if exists "collation_schema";
create schema "collation_schema";
drop schema "collation_schema";

--关键字带单引号-合理报错
drop schema if exists 'collation_schema';
create schema 'collation_schema';

--关键字带反引号-合理报错
drop schema if exists `collation_schema`;
create schema `collation_schema`;

