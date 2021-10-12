--  @testpoint: 分区表global索引，增加和删除分区，查看索引

--建普通表
DROP TABLE if EXISTS test_index_table_173 CASCADE;
create table test_index_table_173(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_173_01;
create index index_173_01 on test_index_table_173(c_int) global;
select relname from pg_class where relname like 'index_173_%';

--增加分区
explain select c_int from test_index_table_173 where c_int > 5000 group by c_int;
ALTER TABLE test_index_table_173 ADD PARTITION P5 VALUES LESS THAN (50000);
explain select c_int from test_index_table_173 where c_int > 5000 group by c_int;
explain select c_int from test_index_table_173 where c_int > 20000 group by c_int;

--删除分区
explain select c_int from test_index_table_173 where c_int < 50 group by c_int;
ALTER TABLE test_index_table_173 drop PARTITION p1;
explain select c_int from test_index_table_173 where c_int < 50 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_173 CASCADE;