--  @testpoint:opengauss关键字transaction_active(非保留)，作为模式名


--关键字不带引号-成功
drop schema if exists transaction_active;
create schema transaction_active;
drop schema transaction_active;

--关键字带双引号-成功
drop schema if exists "transaction_active";
create schema "transaction_active";
drop schema "transaction_active";

--关键字带单引号-合理报错
drop schema if exists 'transaction_active';
create schema 'transaction_active';

--关键字带反引号-合理报错
drop schema if exists `transaction_active`;
create schema `transaction_active`;
