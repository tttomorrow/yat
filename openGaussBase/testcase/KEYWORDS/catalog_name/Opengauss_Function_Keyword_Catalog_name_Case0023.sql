-- @testpoint: opengauss关键字catalog_name非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists catalog_name_test;
create table catalog_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists catalog_name;
create index catalog_name on catalog_name_test(id);

--清理环境
drop index catalog_name;

--关键字带双引号-成功
drop index if exists "catalog_name";
create index "catalog_name" on catalog_name_test(id);

--清理环境
drop index "catalog_name";

--关键字带单引号-合理报错
drop index if exists 'catalog_name';

--关键字带反引号-合理报错
drop index if exists `catalog_name`;
drop table if exists catalog_name_test;