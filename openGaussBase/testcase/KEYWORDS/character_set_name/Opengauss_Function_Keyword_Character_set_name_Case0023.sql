-- @testpoint: opengauss关键字character_set_name非保留)，作为索引名，部分测试点合理报错
--前置条件，创建一个表
drop table if exists character_set_name_test;
create table character_set_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists character_set_name;
create index character_set_name on character_set_name_test(id);

--清理环境
drop index character_set_name;

--关键字带双引号-成功
drop index if exists "character_set_name";
create index "character_set_name" on character_set_name_test(id);

--清理环境
drop index "character_set_name";

--关键字带单引号-合理报错
drop index if exists 'character_set_name';

--关键字带反引号-合理报错
drop index if exists `character_set_name`;
drop table if exists character_set_name_test;