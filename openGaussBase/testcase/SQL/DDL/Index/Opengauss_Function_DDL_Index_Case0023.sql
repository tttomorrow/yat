--  @testpoint: USING method：列存表btree索引：success
--删表
drop table if exists test_index_table_023 cascade;
create table test_index_table_023(id int) WITH (ORIENTATION = column);
--插入数据
BEGIN
  for i in 1..10000 LOOP
    insert into test_index_table_023 values(i);
  end LOOP;
end;
/
--创建索引
drop index if exists index_023;
create index index_023 on test_index_table_023 using btree(id);

--清理数据
drop index if exists index_023;
drop table if exists test_index_table_023 cascade;