--  @testpoint: RENAME TO：修改索引分区名称0位

--建普通表
DROP TABLE if EXISTS test_index_table_138 CASCADE;
create table test_index_table_138(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);


--建索引
drop index if exists index_138_01;
create index index_138_01 on test_index_table_138(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_138_%' order by relname;

--rename
ALTER INDEX if exists index_138_01 RENAME PARTITION p1 TO;

--清理环境
DROP TABLE if EXISTS test_index_table_138 CASCADE;