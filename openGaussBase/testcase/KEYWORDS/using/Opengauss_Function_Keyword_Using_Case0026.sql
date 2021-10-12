--  @testpoint:opengauss关键字using(保留)，作为模式名

--关键字不带引号-合理报错
drop schema if exists using;
create schema using;

--关键字带双引号-成功
drop schema if exists "using";
create schema "using";

--清理环境
drop schema "using";

--关键字带单引号-合理报错
drop schema if exists 'using';
create schema 'using';

--关键字带反引号-合理报错
drop schema if exists `using`;
create schema `using`;

