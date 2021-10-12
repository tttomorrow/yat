--  @testpoint:opengauss关键字having(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source having;

--关键字带双引号-成功
drop data source if exists "having";
create data source "having";
drop data source "having";

--关键字带单引号-合理报错
drop data source if exists 'having';
create data source 'having';

--关键字带反引号-合理报错
drop data source if exists `having`;
create data source `having`;
