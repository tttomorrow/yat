--  @testpoint: where:引用表中不存在的列

DROP TABLE if EXISTS test_index_table_099 CASCADE;
create table test_index_table_099(
c_float1 float
) WITH (ORIENTATION = row) ;


--建btree索引:5-5
drop index if exists index_099_01;
create index index_099_01 on test_index_table_099 using btree(c_float1) where c_int >10;
select relname from pg_class where relname like 'index_099_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_099 CASCADE;