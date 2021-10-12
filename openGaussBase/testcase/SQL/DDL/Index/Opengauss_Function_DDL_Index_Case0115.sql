--  @testpoint:RENAME TO：修改索引名称64位

--创建表
DROP TABLE if EXISTS test_index_table_115 CASCADE;
create table test_index_table_115(
c_int int
) WITH (ORIENTATION = row) ;


--建索引
drop index if exists index_115;
create index index_115 on test_index_table_115(c_int);
select relname from pg_class where relname like 'index_115%' order by relname;

--rename

--清理环境
DROP TABLE if EXISTS test_index_table_115 CASCADE;