-- @testpoint: opengauss关键字like(保留)，作为序列名 合理报错


--关键字不带引号-合理报错
drop sequence if exists like;
create sequence like start 100 cache 50;

--关键字带双引号-成功
drop sequence if exists "like";
create sequence "like" start 100 cache 50;

--清理环境
drop sequence "like";

--关键字带单引号-合理报错
drop sequence if exists 'like';
create sequence 'like' start 100 cache 50;

--关键字带反引号-合理报错
drop sequence if exists `like`;
create sequence `like` start 100 cache 50;
