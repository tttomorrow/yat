--  @testpoint: RENAME TO：修改索引名称0位

--创建表
DROP TABLE if EXISTS test_index_table_113 CASCADE;
create table test_index_table_113(
c_int int
) WITH (ORIENTATION = row) ;

--建索引
drop index if exists index_113;
create index index_113 on test_index_table_113(c_int);
select relname from pg_class where relname like 'index_113%' order by relname;

--rename
ALTER index IF EXISTS index_113 RENAME TO ;

--清理环境
DROP TABLE if EXISTS test_index_table_113 CASCADE;