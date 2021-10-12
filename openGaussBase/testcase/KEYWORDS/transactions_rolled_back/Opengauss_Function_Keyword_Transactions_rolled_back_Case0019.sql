--  @testpoint:opengauss关键字transactions_rolled_back(非保留)，作为外部数据源名

--关键字不带引号-成功
drop data source if exists transactions_rolled_back;
create data source transactions_rolled_back;
drop data source transactions_rolled_back;

--关键字带双引号-成功
drop data source if exists "transactions_rolled_back";
create data source "transactions_rolled_back";
drop data source "transactions_rolled_back";

--关键字带单引号-合理报错
drop data source if exists 'transactions_rolled_back';
create data source 'transactions_rolled_back';

--关键字带反引号-合理报错
drop data source if exists `transactions_rolled_back`;
create data source `transactions_rolled_back`;
