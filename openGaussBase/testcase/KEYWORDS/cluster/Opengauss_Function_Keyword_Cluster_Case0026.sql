--  @testpoint:opengauss关键字cluster(非保留)，作为模式名
--关键字不带引号-成功
drop schema if exists cluster;
create schema cluster;

--清理环境
drop schema cluster;

--关键字带双引号-成功
drop schema if exists "cluster";
create schema "cluster";

--清理环境
drop schema "cluster";

--关键字带单引号-合理报错
drop schema if exists 'cluster';

--关键字带反引号-合理报错
drop schema if exists `cluster`;
