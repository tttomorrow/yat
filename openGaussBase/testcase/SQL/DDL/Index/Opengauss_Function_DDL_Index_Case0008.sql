--  @testpoint: create index:table_name：为不存在的表创建index：合理报错
--删表
drop table if exists test_index_schema_01 cascade;
--创建索引
drop index if exists schema_index_01;
create index schema_index_01 on test_index_schema_01(id);