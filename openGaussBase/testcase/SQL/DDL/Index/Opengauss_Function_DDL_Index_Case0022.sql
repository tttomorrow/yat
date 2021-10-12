--  @testpoint: USING method：行存表psort索引：合理报错
--删表
drop table if exists test_index_table_022 cascade;
create table test_index_table_022(id int) WITH (ORIENTATION = row);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_022 values(i);
  end LOOP;
end;
/
--创建索引
drop index if exists index_022;
create index index_022 on test_index_table_022 using psort(id);
--清理数据
drop index if exists index_022;
drop table if exists test_index_table_022 cascade;