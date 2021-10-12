-- @testpoint: USING method：列存local分区表psort组合索引：success
--删表
drop table if exists test_index_table_042 cascade;
create table test_index_table_042(id int,name varchar) WITH (ORIENTATION = column)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--插入数据
BEGIN
  for i in 1..2000 LOOP
    insert into test_index_table_042 values(i);
  end LOOP;
end;
/
explain select * from test_index_table_042 where id = 1985;
--创建索引
drop index if exists index_042;
create index index_042 on test_index_table_042 using psort(id, name) LOCAL;
explain select * from test_index_table_042 where id = 1985;
select relname from pg_class where relname='index_042';
--清理数据
drop index if exists index_042;
drop table if exists test_index_table_042 cascade;