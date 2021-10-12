--  @testpoint: with：psort不支持FILLFACTOR
DROP TABLE if EXISTS test_index_table_093 CASCADE;
create table test_index_table_093(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort索引:fillfactor 100
drop index if exists index_093_01;
create index index_093_01 on test_index_table_093(c_float1) with (fillfactor=100);
select relname from pg_class where relname like 'index_093_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_093 CASCADE;