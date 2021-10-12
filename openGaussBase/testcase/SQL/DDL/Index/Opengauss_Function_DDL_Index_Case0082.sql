--  @testpoint: expression：列存psort和btree不支持表达式索引

DROP TABLE if EXISTS test_index_table_082 CASCADE;
create table test_index_table_082(
c_float1 float
) WITH (ORIENTATION = column) ;

--建psort索引：合理报错
drop index if exists index_082_01;
create index index_082_01 on test_index_table_082 using psort(lower(c_float1));
select relname from pg_class where relname like 'index_082_%' order by relname;

--建psort索引：合理报错
drop index if exists index_082_01;
create index index_082_01 on test_index_table_082 using btree(lower(c_float1));
select relname from pg_class where relname like 'index_082_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_082 CASCADE;