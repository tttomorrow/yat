--  @testpoint: RENAME TO：修改索引名称为含非法字符

--创建表
DROP TABLE if EXISTS test_index_table_117 CASCADE;
create table test_index_table_117(
c_int int
) WITH (ORIENTATION = row) ;

--建索引
drop index if exists index_117_01;
drop index if exists index_117_02;
create index index_117_01 on test_index_table_117(c_int);
create index index_117_02 on test_index_table_117(c_int);
select relname from pg_class where relname like 'index_117%' order by relname;

--rename
ALTER index index_117_01 RENAME TO index@@;
ALTER index index_117_01 RENAME TO index!!;
ALTER index index_117_01 RENAME TO 117index;
ALTER index index_117_01 RENAME TO $index;
ALTER index index_117_01 RENAME TO ind ex;
ALTER index index_117_01 RENAME TO index"";
ALTER index index_117_01 RENAME TO index();
ALTER index index_117_01 RENAME TO index==;
select relname from pg_class where relname like 'index_117%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_117 CASCADE;
