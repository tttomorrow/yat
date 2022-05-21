--  @testpoint: RENAME PARTITION：修改索引名称1-63位

--建普通表
DROP TABLE if EXISTS test_index_table_139 CASCADE;
create table test_index_table_139(
c_int int
) WITH (ORIENTATION = column) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引
drop index if exists index_139_01;
create index index_139_01 on test_index_table_139(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_139_%' order by relname;

--rename
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_139_01') order by relname asc;
ALTER INDEX if exists index_139_01 RENAME PARTITION p1 TO p12345678901324567890132456789012345678901234567890123456789012;
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_139_01') order by relname asc;
ALTER INDEX if exists index_139_01 RENAME PARTITION p12345678901324567890132456789012345678901234567890123456789012 TO p1;
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_139_01') order by relname asc;

--清理环境
DROP TABLE if EXISTS test_index_table_139 CASCADE;