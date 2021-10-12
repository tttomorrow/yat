--  @testpoint: set：FILLFACTOR:无效值：合理报错

DROP TABLE if EXISTS test_index_table_124 CASCADE;
create table test_index_table_124(
c_float1 float
) WITH (ORIENTATION = row) ;


--建btree索引
drop index if exists index_124_01;
create index index_124_01 on test_index_table_124(c_float1) with (fillfactor=50);
select relname from pg_class where relname like 'index_124_%' order by relname;

--set
alter index index_124_01 set (fillfactor=9);
alter index index_124_01 set (fillfactor=101);
alter index index_124_01 set (fillfactor=50.5);
alter index index_124_01 set (fillfactor='test');
alter index index_124_01 set (fillfactor='$%_#');

--清理环境
DROP TABLE if EXISTS test_index_table_124 CASCADE;