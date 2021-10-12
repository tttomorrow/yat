--  @testpoint:opengauss关键字schema非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists schema;
create sequence schema start 100 cache 50;
drop sequence schema;

--关键字带双引号-成功
drop sequence if exists "schema";
create sequence "schema" start 100 cache 50;
drop sequence "schema";

--关键字带单引号-合理报错
drop sequence if exists 'schema';
create sequence 'schema' start 100 cache 50;

--关键字带反引号-合理报错
drop sequence if exists `schema`;
create sequence `schema` start 100 cache 50;
