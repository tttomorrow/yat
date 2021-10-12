--  @testpoint:opengauss关键字ada(非保留)，作为序列名
--关键字不带引号-成功
drop sequence if exists ada;
create sequence ada start 100 cache 50;

--清理环境
drop sequence ada;

--关键字带双引号-成功
drop sequence if exists "ada";
create sequence "ada" start 100 cache 50;

--清理环境
drop sequence "ada";

--关键字带单引号-合理报错
drop sequence if exists 'ada';

--关键字带反引号-合理报错
drop sequence if exists `ada`;
