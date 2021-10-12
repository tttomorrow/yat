--  @testpoint:opengauss关键字binary_double非保留)，作为序列名
--关键字不带引号-成功
drop sequence if exists binary_double;
create sequence binary_double start 100 cache 50;

--清理环境
drop sequence binary_double;

--关键字带双引号-成功
drop sequence if exists "binary_double";
create sequence "binary_double" start 100 cache 50;

--清理环境
drop sequence "binary_double";

--关键字带单引号-合理报错
drop sequence if exists 'binary_double';

--关键字带反引号-合理报错
drop sequence if exists `binary_double`;
