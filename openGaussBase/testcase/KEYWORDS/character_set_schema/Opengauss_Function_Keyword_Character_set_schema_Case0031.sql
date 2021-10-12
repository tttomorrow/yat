--  @testpoint:opengauss关键字character_set_schema(非保留)，作为字段数据类型(合理报错)
--前置条件
drop table if exists character_set_schema_test cascade;

--关键字不带引号-合理报错
create table character_set_schema_test(id int,name character_set_schema);

--关键字带双引号-合理报错
create table character_set_schema_test(id int,name "character_set_schema");

--关键字带单引号-合理报错
create table character_set_schema_test(id int,name 'character_set_schema');

--关键字带反引号-合理报错
create table character_set_schema_test(id int,name `character_set_schema`);
