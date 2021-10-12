--  @testpoint:opengauss关键字public非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists public;
create sequence public start 100 cache 50;
drop sequence public;

--关键字带双引号-成功
drop sequence if exists "public";
create sequence "public" start 100 cache 50;
drop sequence "public";

--关键字带单引号-合理报错
drop sequence if exists 'public';

--关键字带反引号-合理报错
drop sequence if exists `public`;

