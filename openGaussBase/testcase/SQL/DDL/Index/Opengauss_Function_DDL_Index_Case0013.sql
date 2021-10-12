-- @testpoint:  create index:table_name：行存分区表的index：支持全局分区索引
--删表
drop table if exists test_index_table_01 cascade;
create table test_index_table_01(id int) WITH (ORIENTATION = row)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--插入数据
BEGIN
  for i in 1..2000 LOOP
    insert into test_index_table_01 values(i);
  end LOOP;
end;
/
explain select * from test_index_table_01 where id = 1985;
--创建索引
drop index if exists partition_index_01;
create index partition_index_01 on test_index_table_01(id);

--清理数据
drop index if exists schema_index_01;
drop table if exists test_index_table_01 cascade;
