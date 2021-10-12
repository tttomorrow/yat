--  @testpoint:opengauss关键字reloptions非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists reloptions;
create sequence reloptions start 100 cache 50;
drop sequence reloptions;

--关键字带双引号-成功
drop sequence if exists "reloptions";
create sequence "reloptions" start 100 cache 50;
drop sequence "reloptions";

--关键字带单引号-合理报错
drop sequence if exists 'reloptions';

--关键字带反引号-合理报错
drop sequence if exists `reloptions`;

