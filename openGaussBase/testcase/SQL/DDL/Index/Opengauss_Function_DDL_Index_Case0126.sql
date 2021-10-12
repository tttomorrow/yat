--  @testpoint: set：psort，btree，gist不支持GIN_PENDING_LIST_LIMIT

DROP TABLE if EXISTS test_index_table_126 CASCADE;
create table test_index_table_126(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort+gist索引
drop index if exists index_126_01;
create index index_126_01 on test_index_table_126 using psort(c_float1) ;
select relname from pg_class where relname like 'index_126_%' order by relname;

--set
alter index index_126_01 set (GIN_PENDING_LIST_LIMIT='64KB');

DROP TABLE if EXISTS test_index_table_126 CASCADE;
create table test_index_table_126(
c_float1 float,
c_point point
) WITH (ORIENTATION = row) ;

--建btree+gist索引
drop index if exists index_126_01;
drop index if exists index_126_02;
create index index_126_01 on test_index_table_126 using btree(c_float1) ;
create index index_126_02 on test_index_table_126 using gist(c_point) ;
select relname from pg_class where relname like 'index_126_%' order by relname;

--set
alter index index_126_01 set (GIN_PENDING_LIST_LIMIT='64KB');
alter index index_126_02 set (GIN_PENDING_LIST_LIMIT='64KB');

--清理环境
DROP TABLE if EXISTS test_index_table_126 CASCADE;