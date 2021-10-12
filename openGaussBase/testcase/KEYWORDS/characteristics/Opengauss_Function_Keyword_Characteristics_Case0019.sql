--  @testpoint:opengauss关键字characteristics(非保留)，作为外部数据源名
--关键字不带引号-成功
drop data source if exists characteristics;
create data source characteristics;

--清理环境
drop data source characteristics;

--关键字带双引号-成功
drop data source if exists "characteristics";
create data source "characteristics";

--清理环境
drop data source "characteristics";

--关键字带单引号-合理报错
drop data source if exists 'characteristics';

--关键字带反引号-合理报错
drop data source if exists `characteristics`;
