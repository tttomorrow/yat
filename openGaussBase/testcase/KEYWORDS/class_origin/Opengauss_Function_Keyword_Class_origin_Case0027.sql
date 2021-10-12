--  @testpoint:opengauss关键字class_origin非保留)，作为序列名
--关键字不带引号-成功
drop sequence if exists class_origin;
create sequence class_origin start 100 cache 50;

--清理环境
drop sequence class_origin;

--关键字带双引号-成功
drop sequence if exists "class_origin";
create sequence "class_origin" start 100 cache 50;

--清理环境
drop sequence "class_origin";

--关键字带单引号-合理报错
drop sequence if exists 'class_origin';

--关键字带反引号-合理报错
drop sequence if exists `class_origin`;
