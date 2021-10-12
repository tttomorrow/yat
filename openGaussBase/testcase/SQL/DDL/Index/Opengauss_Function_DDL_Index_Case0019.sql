-- @testpoint:  create index:table_name：列存分区表的global index：合理报错
--删表
drop table if exists test_index_table_019 cascade;
create table test_index_table_019(id int) WITH (ORIENTATION = column)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--插入数据
BEGIN
  for i in 1..2000 LOOP
    insert into test_index_table_019 values(i);
  end LOOP;
end;
/
explain select * from test_index_table_019 where id = 1985;
--创建索引
drop index if exists partition_index_019;
create index partition_index_019 on test_index_table_019(id) global;
select relname from pg_class where relname='partition_index_019';

--清理数据
drop index if exists partition_index_019;
drop table if exists test_index_table_019 cascade;
