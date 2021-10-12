--  @testpoint:opengauss关键字action(非保留)，作为序列名
--关键字不带引号-成功
drop sequence if exists action;
create sequence action start 100 cache 50;

--清理环境
drop sequence action;

--关键字带双引号-成功
drop sequence if exists "action";
create sequence "action" start 100 cache 50;

--清理环境
drop sequence "action";

--关键字带单引号-合理报错
drop sequence if exists 'action';

--关键字带反引号-合理报错
drop sequence if exists `action`;
