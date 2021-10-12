--  @testpoint:opengauss关键字cluster(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists cluster;
create data source cluster;

--清理环境
drop data source cluster;

--关键字带双引号-成功
drop data source if exists "cluster";
create data source "cluster";

--清理环境
drop data source "cluster";

--关键字带单引号-合理报错
drop data source if exists 'cluster';

--关键字带反引号-合理报错
drop data source if exists `cluster`;
