-- @testpoint: where:引用另一张表的列:合理报错

DROP TABLE if EXISTS test_index_table_102 CASCADE;
create table test_index_table_102(
c_float1 float,
c_int int,
c_varchar varchar,
c_text text
) WITH (ORIENTATION = row) ;

DROP TABLE if EXISTS test_index_table_102_02 CASCADE;
create table test_index_table_102_02(
c_float1 float,
c_int int,
c_varchar varchar,
c_text text
) WITH (ORIENTATION = row) ;


--建索引
drop index if exists index_102_01;
create index index_102_01 on test_index_table_102(c_float1) where test_index_table_102_02.c_int >10 ;
select relname from pg_class where relname like 'index_102_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_102 CASCADE;
DROP TABLE if EXISTS test_index_table_102_02 CASCADE;