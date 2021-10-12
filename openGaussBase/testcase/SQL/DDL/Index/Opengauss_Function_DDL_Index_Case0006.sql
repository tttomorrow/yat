-- @testpoint: create index:模式名的标识符规范：不存在的模式名：合理报错

drop schema if exists testschema cascade;

drop table if exists testschema.test_index_schema_01 cascade;
drop table if exists test_index_schema_01 cascade;
create table test_index_schema_01(id int);
--建索引
drop index if exists testschema.schema_index_01;
create index testschema.schema_index_01 on test_index_schema_01(id);

--清理数据
drop table if exists test_index_schema_01 cascade;
drop schema if exists testschema cascade;
