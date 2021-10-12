--  @testpoint:with：psort，btree，gist不支持FASTUPDATE

DROP TABLE if EXISTS test_index_table_095 CASCADE;
create table test_index_table_095(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort+gist索引
drop index if exists index_095_01;
create index index_095_01 on test_index_table_095 using psort(c_float1) with (FASTUPDATE=on);
create index index_095_01 on test_index_table_095 using gist(c_float1) with (FASTUPDATE=on);
select relname from pg_class where relname like 'index_095_%' order by relname;

DROP TABLE if EXISTS test_index_table_095 CASCADE;
create table test_index_table_095(
c_float1 float,
c_point point
) WITH (ORIENTATION = row) ;

--建btree+gist索引
drop index if exists index_095_01;
create index index_095_01 on test_index_table_095 using btree(c_float1) with (FASTUPDATE=on);
create index index_095_01 on test_index_table_095 using gist(c_point) with (FASTUPDATE=on);
select relname from pg_class where relname like 'index_095_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_095 CASCADE;