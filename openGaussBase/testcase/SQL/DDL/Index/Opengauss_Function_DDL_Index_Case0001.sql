-- @testpoint: create index:模式名为0位:success
--不引用模式建表
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
drop index if exists schema_index_01;
create index schema_index_01 on test_index_schema_01(id);
explain select * from test_index_schema_01 where id = 999;

--清理数据
drop table if exists test_index_schema_01 cascade;
drop index if exists schema_index_01 cascade;