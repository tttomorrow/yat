--  @testpoint:分区表local索引，增加和删除分区，增加索引

--建普通表
DROP TABLE if EXISTS test_index_table_174 CASCADE;
create table test_index_table_174(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_174_01;
create index index_174_01 on test_index_table_174(c_int) local (partition p1,partition p2,partition p3,partition p4);
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_174_01') order by relname asc;
--增加分区
explain select c_int from test_index_table_174 where c_int > 5000 group by c_int;
ALTER TABLE test_index_table_174 ADD PARTITION P5 VALUES LESS THAN (50000);
explain select c_int from test_index_table_174 where c_int > 20000 group by c_int;
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_174_01') order by relname asc;

--删除分区
explain select c_int from test_index_table_174 where c_int < 50 group by c_int;
ALTER TABLE test_index_table_174 drop PARTITION p1;
explain select c_int from test_index_table_174 where c_int < 50 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_174 CASCADE;