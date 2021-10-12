--  @testpoint:opengauss关键字message_octet_length(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists message_octet_length;
create data source message_octet_length;
drop data source message_octet_length;

--关键字带双引号-成功
drop data source if exists "message_octet_length";
create data source "message_octet_length";
drop data source "message_octet_length";

--关键字带单引号-合理报错
drop data source if exists 'message_octet_length';
create data source 'message_octet_length';

--关键字带反引号-合理报错
drop data source if exists `message_octet_length`;
create data source `message_octet_length`;
