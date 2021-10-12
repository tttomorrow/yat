--  @testpoint:with：psort，btree，gist不支持GIN_PENDING_LIST_LIMIT

DROP TABLE if EXISTS test_index_table_094 CASCADE;
create table test_index_table_094(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort+gist索引
drop index if exists index_094_01;
create index index_094_01 on test_index_table_094 using psort(c_float1) with (GIN_PENDING_LIST_LIMIT='64KB');
create index index_094_01 on test_index_table_094 using gist(c_float1) with (GIN_PENDING_LIST_LIMIT='64KB');
select relname from pg_class where relname like 'index_094_%' order by relname;

DROP TABLE if EXISTS test_index_table_094 CASCADE;
create table test_index_table_094(
c_float1 float,
c_point point
) WITH (ORIENTATION = row) ;

--建btree+gist索引
drop index if exists index_094_01;
create index index_094_01 on test_index_table_094 using btree(c_float1) with (GIN_PENDING_LIST_LIMIT='64KB');
create index index_094_01 on test_index_table_094 using gist(c_point) with (GIN_PENDING_LIST_LIMIT='64KB');
select relname from pg_class where relname like 'index_094_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_094 CASCADE;