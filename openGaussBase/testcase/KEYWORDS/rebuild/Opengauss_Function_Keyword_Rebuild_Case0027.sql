--  @testpoint:opengauss关键字rebuild非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists rebuild;
create sequence rebuild start 100 cache 50;
drop sequence rebuild;

--关键字带双引号-成功
drop sequence if exists "rebuild";
create sequence "rebuild" start 100 cache 50;
drop sequence "rebuild";

--关键字带单引号-合理报错
drop sequence if exists 'rebuild';

--关键字带反引号-合理报错
drop sequence if exists `rebuild`;

