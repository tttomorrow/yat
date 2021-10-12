--  @testpoint:opengauss关键字bit_length(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists bit_length;
create data source bit_length;

--清理环境
drop data source bit_length;

--关键字带双引号-成功
drop data source if exists "bit_length";
create data source "bit_length";

--清理环境
drop data source "bit_length";

--关键字带单引号-合理报错
drop data source if exists 'bit_length';

--关键字带反引号-合理报错
drop data source if exists `bit_length`;
