-- @testpoint:  create index:表无模式和index有模式，不在同一模式：合理报错
drop schema if exists testschema cascade;
create schema testschema;
drop table if exists test_index_schema_01 cascade;
create table test_index_schema_01(id int);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_schema_01 values(i);
  end LOOP;
end;
/
explain select * from test_index_schema_01 where id = 1;
--建索引
drop index if exists testschema.schema_index_01;
create index testschema.schema_index_01 on test_index_schema_01(id);

--清理数据
drop index if exists testschema.schema_index_01 cascade;
drop table if exists test_index_schema_01 cascade;
drop schema if exists testschema cascade;