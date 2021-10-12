--  @testpoint:create index CONCURRENTLY：列存表和分区表不支持：合理报错
--建行存分区表
DROP TABLE if EXISTS test_index_table_193 CASCADE;
create table test_index_table_193(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引
drop index if exists index_193_01;
create index CONCURRENTLY index_193_01 on test_index_table_193(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
create index CONCURRENTLY index_193_01 on test_index_table_193(c_int) ;

--行存临时分区表

--建列存表分区表
DROP TABLE if EXISTS test_index_table_193 CASCADE;
create table test_index_table_193(
c_int int
) WITH (ORIENTATION = column) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引
drop index if exists index_193_01;
create index CONCURRENTLY index_193_01 on test_index_table_193(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
create index CONCURRENTLY index_193_01 on test_index_table_193(c_int) ;

--建列存表
DROP TABLE if EXISTS test_index_table_193 CASCADE;
create table test_index_table_193(
c_int int
) WITH (ORIENTATION = column) ;

--建索引
drop index if exists index_193_01;
create index CONCURRENTLY index_193_01 on test_index_table_193(c_int) ;

--清理环境
DROP TABLE if EXISTS test_index_table_193 CASCADE;

--建列存临时表
DROP TABLE if EXISTS test_index_table_193 CASCADE;
create temporary table test_index_table_193(
c_int int
) WITH (ORIENTATION = column) ;

--建索引
drop index if exists index_193_01;
create index CONCURRENTLY index_193_01 on test_index_table_193(c_int) ;

--清理环境
DROP TABLE if EXISTS test_index_table_193 CASCADE;

