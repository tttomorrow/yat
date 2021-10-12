--  @testpoint: set：psort，btree，gist不支持FASTUPDATE

DROP TABLE if EXISTS test_index_table_127 CASCADE;
create table test_index_table_127(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort+gist索引
drop index if exists index_127_01;
create index index_127_01 on test_index_table_127 using psort(c_float1) ;
select relname from pg_class where relname like 'index_127_%' order by relname;

--set
alter index index_127_01 set  (FASTUPDATE=on);

DROP TABLE if EXISTS test_index_table_127 CASCADE;
create table test_index_table_127(
c_float1 float,
c_point point
) WITH (ORIENTATION = row) ;

--建btree+gist索引
drop index if exists index_127_01;
drop index if exists index_127_02;
create index index_127_01 on test_index_table_127 using btree(c_float1) ;
create index index_127_02 on test_index_table_127 using gist(c_point) ;
select relname from pg_class where relname like 'index_127_%' order by relname;

--set
alter index index_127_01 set  (FASTUPDATE=on);
alter index index_127_02 set  (FASTUPDATE=on);

--清理环境
DROP TABLE if EXISTS test_index_table_127 CASCADE;