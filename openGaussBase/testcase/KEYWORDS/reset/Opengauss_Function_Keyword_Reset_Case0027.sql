--  @testpoint:opengauss关键字reset非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists reset;
create sequence reset start 100 cache 50;
drop sequence reset;

--关键字带双引号-成功
drop sequence if exists "reset";
create sequence "reset" start 100 cache 50;
drop sequence "reset";

--关键字带单引号-合理报错
drop sequence if exists 'reset';

--关键字带反引号-合理报错
drop sequence if exists `reset`;

