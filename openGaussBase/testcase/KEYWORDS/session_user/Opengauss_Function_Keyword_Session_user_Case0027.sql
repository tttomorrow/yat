--  @testpoint:opengauss关键字session_user(保留)，作为序列名


--关键字不带引号-合理报错
drop sequence if exists session_user;
create sequence session_user start 100 cache 50;

--关键字带双引号-成功
drop sequence if exists "session_user";
create sequence "session_user" start 100 cache 50;

--清理环境
drop sequence "session_user";

--关键字带单引号-合理报错
drop sequence if exists 'session_user';
create sequence 'session_user' start 100 cache 50;

--关键字带反引号-合理报错
drop sequence if exists `session_user`;
create sequence `session_user` start 100 cache 50;
