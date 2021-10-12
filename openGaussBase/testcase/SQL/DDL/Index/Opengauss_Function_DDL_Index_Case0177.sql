--  @testpoint:并分区查看索引

--建普通表
DROP TABLE if EXISTS test_index_table_177 CASCADE;
create table test_index_table_177(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_177_01;
create index index_177_01 on test_index_table_177(c_int) local (partition p1,partition p2,partition p3,partition p4);
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_177_01') order by relname asc;

--并分区,切割分区查看索引
alter table test_index_table_177 merge partitions p1,p2 into partition p2;
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_177_01') order by relname asc;
alter table test_index_table_177 split partition p2 at (500)INTO (PARTITION p0,partition p1);
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_177_01') order by relname asc;

--清理环境
DROP TABLE if EXISTS test_index_table_177 CASCADE;
