--  @testpoint: set：psort不支持FILLFACTOR

DROP TABLE if EXISTS test_index_table_125 CASCADE;
create table test_index_table_125(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort索引:fillfactor 100
drop index if exists index_125_01;
create index index_125_01 on test_index_table_125(c_float1);
select relname from pg_class where relname like 'index_125_%' order by relname;

--set
alter index index_125_01 set (fillfactor=100);
--清理环境
DROP TABLE if EXISTS test_index_table_125 CASCADE;