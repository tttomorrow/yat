--  @testpoint: with：FILLFACTOR:无效值：合理报错
DROP TABLE if EXISTS test_index_table_092 CASCADE;
create table test_index_table_092(
c_float1 float
) WITH (ORIENTATION = row) ;


--建btree索引:fillfactor 101
drop index if exists index_092_01;
create index index_092_01 on test_index_table_092(c_float1) with (fillfactor=101);
select relname from pg_class where relname like 'index_092_%' order by relname;

--建btree索引:fillfactor 9
drop index if exists index_092_01;
create index index_092_01 on test_index_table_092(c_float1) with (fillfactor=9);
select relname from pg_class where relname like 'index_092_%' order by relname;

--建btree索引:fillfactor 50.5
drop index if exists index_092_01;
create index index_092_01 on test_index_table_092(c_float1) with (fillfactor=50.5);
select relname from pg_class where relname like 'index_092_%' order by relname;

--建btree索引:fillfactor test
drop index if exists index_092_01;
create index index_092_01 on test_index_table_092(c_float1) with (fillfactor='test');
select relname from pg_class where relname like 'index_092_%' order by relname;

--建btree索引:fillfactor $%_#
drop index if exists index_092_01;
create index index_092_01 on test_index_table_092(c_float1) with (fillfactor='$%_#');
select relname from pg_class where relname like 'index_092_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_092 CASCADE;