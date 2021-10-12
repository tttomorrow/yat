--  @testpoint:opengauss关键字session_user(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source session_user;

--关键字带双引号-成功
drop data source if exists "session_user";
create data source "session_user";
drop data source "session_user";

--关键字带单引号-合理报错
drop data source if exists 'session_user';
create data source 'session_user';

--关键字带反引号-合理报错
drop data source if exists `session_user`;
create data source `session_user`;
