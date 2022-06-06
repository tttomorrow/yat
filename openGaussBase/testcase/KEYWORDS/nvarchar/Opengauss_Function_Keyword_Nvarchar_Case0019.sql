-- @testpoint: opengauss关键字nvarchar(非保留)，作为外部数据源名 部分测试点合理报错

--step1:关键字不带引号;expect:成功
drop data source if exists nvarchar;
create data source nvarchar;
drop data source nvarchar;

--step2:关键字带双引号;expect:成功
drop data source if exists "nvarchar";
create data source "nvarchar";
drop data source "nvarchar";

--step3:关键字带单引号;expect:合理报错
drop data source if exists 'nvarchar';
create data source 'nvarchar';

--step4:关键字带反引号;expect:合理报错
drop data source if exists `nvarchar`;
create data source `nvarchar`;