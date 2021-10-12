-- @testpoint: 改分区名称并通过索引查询

--建普通表
DROP TABLE if EXISTS test_index_table_176 CASCADE;
create table test_index_table_176(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_176_01;
create index index_176_01 on test_index_table_176(c_int) local (partition p1,partition p2,partition p3,partition p4);
select relname from pg_class where relname like 'index_176_%';

--重命名
explain select c_int from test_index_table_176 where c_int > 50 group by c_int;
alter table test_index_table_176  rename Partition  p1 to p5;
explain select c_int from test_index_table_176 where c_int > 50 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_176_01 CASCADE;
DROP TABLE if EXISTS test_index_table_176 CASCADE;

