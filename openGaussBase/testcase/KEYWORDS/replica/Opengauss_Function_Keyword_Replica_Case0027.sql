--  @testpoint:opengauss关键字replica非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists replica;
create sequence replica start 100 cache 50;
drop sequence replica;

--关键字带双引号-成功
drop sequence if exists "replica";
create sequence "replica" start 100 cache 50;
drop sequence "replica";

--关键字带单引号-合理报错
drop sequence if exists 'replica';

--关键字带反引号-合理报错
drop sequence if exists `replica`;

