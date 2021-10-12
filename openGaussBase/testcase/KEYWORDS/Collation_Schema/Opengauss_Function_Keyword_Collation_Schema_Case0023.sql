-- @testpoint: opengauss关键字collation_schema(非保留)，作为索引名 合理报错

--前置条件，创建一个表
drop table if exists collation_schema_test;
create table collation_schema_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists collation_schema;
create index collation_schema on collation_schema_test(id);
drop index collation_schema;

--关键字带双引号-成功
drop index if exists "collation_schema";
create index "collation_schema" on collation_schema_test(id);
drop index "collation_schema";

--关键字带单引号-合理报错
drop index if exists 'collation_schema';
create index 'collation_schema' on collation_schema_test(id);

--关键字带反引号-合理报错
drop index if exists `collation_schema`;
create index `collation_schema` on collation_schema_test(id);
drop table if exists collation_schema_test;