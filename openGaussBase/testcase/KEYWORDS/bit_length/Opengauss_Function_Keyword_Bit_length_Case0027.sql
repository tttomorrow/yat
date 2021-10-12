--  @testpoint:opengauss关键字bit_length非保留)，作为序列名
--关键字不带引号-成功
drop sequence if exists bit_length;
create sequence bit_length start 100 cache 50;

--清理环境
drop sequence bit_length;

--关键字带双引号-成功
drop sequence if exists "bit_length";
create sequence "bit_length" start 100 cache 50;

--清理环境
drop sequence "bit_length";

--关键字带单引号-合理报错
drop sequence if exists 'bit_length';

--关键字带反引号-合理报错
drop sequence if exists `bit_length`;
