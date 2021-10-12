--  @testpoint:opengauss关键字from(保留)，作为外部数据源名

--关键字不带引号-合理报错
create data source from;

--关键字带双引号-成功
drop data source if exists "from";
create data source "from";
drop data source "from";

--关键字带单引号-合理报错
drop data source if exists 'from';
create data source 'from';

--关键字带反引号-合理报错
drop data source if exists `from`;
create data source `from`;
