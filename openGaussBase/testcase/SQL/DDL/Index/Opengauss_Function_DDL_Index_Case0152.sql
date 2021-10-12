--  @testpoint: DROP INDEX CONCURRENTLY 指定多个索引

--建普通表
DROP TABLE if EXISTS test_index_table_152 CASCADE;
create table test_index_table_152(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引
drop index if exists index_152_01;
drop index if exists index_152_02;
create index index_152_01 on test_index_table_152(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
create index index_152_02 on test_index_table_152(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_152_%' order by relname;

--DROP INDEX CONCURRENTLY
DROP INDEX CONCURRENTLY index_152_01,index_152_02;

--清理环境
DROP TABLE if EXISTS test_index_table_152 CASCADE;