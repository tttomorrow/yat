-- @testpoint: RENAME TO：修改索引名称为索引同义词名称

--创建表
DROP TABLE if EXISTS test_index_table_118 CASCADE;
create table test_index_table_118(
c_int int
) WITH (ORIENTATION = row) ;

--建索引
drop index if exists index_118_01;
create index index_118_01 on test_index_table_118(c_int);
select relname from pg_class where relname like 'index_118%' order by relname;

--建同义词
drop synonym if exists syn_index_118_01;
create synonym  syn_index_118_01 for index_118_01;

--通过同义词rename
ALTER index index_118_01 RENAME TO syn_index_118_01;
select relname from pg_class where relname like '%index_118%' order by relname;

--清理环境
drop synonym if exists syn_index_118_01;
DROP TABLE if EXISTS test_index_table_118 CASCADE;
