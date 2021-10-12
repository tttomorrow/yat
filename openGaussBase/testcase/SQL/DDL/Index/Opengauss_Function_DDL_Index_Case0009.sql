-- @testpoint:  create index:table_name：使用表名的同义词创建index：success
--删表
drop table if exists test_index_table_01 cascade;
create table test_index_table_01(id int);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_01 values(i);
  end LOOP;
end;
/
--建同义词
drop synonym if exists syn_test_index_table_01;
create synonym syn_test_index_table_01 for test_index_table_01;
explain select * from syn_test_index_table_01 where id = 1;
--创建索引
drop index if exists schema_index_01;
create index schema_index_01 on syn_test_index_table_01(id);
explain select * from syn_test_index_table_01 where id = 1;
--清理数据
drop synonym if exists syn_test_index_table_01;
drop index if exists schema_index_01;
drop table if exists test_index_table_01 cascade;