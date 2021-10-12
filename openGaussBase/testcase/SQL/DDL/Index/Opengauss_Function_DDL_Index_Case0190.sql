--  @testpoint: reindex：行存表使用REINDEX INTERNAL TABLE：合理报错

DROP TABLE if EXISTS test_index_table_190 CASCADE;
create table test_index_table_190(
c_int1 int
) with (orientation = row);

--建btree索引:
drop index if exists index_190_01;
create index index_190_01 on test_index_table_190 using btree(c_int1);
select relname from pg_class where relname like 'index_190_%' order by relname;

--重建
REINDEX INTERNAL TABLE test_index_table_190;

--清理环境
DROP TABLE if EXISTS test_index_table_190 CASCADE;