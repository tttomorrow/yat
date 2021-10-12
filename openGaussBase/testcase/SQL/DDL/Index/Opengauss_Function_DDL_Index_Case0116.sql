--  @testpoint: RENAME TO：修改索引名称为已存在索引名称

--创建表
DROP TABLE if EXISTS test_index_table_116 CASCADE;
create table test_index_table_116(
c_int int
) WITH (ORIENTATION = row) ;

--建索引
drop index if exists index_116_01;
drop index if exists index_116_02;
create index index_116_01 on test_index_table_116(c_int);
create index index_116_02 on test_index_table_116(c_int);
select relname from pg_class where relname like 'index_116%' order by relname;

--rename
--不存在
ALTER index index_116 RENAME TO index_116_01;
ALTER index IF EXISTS index_116 RENAME TO index_116_01;
--同名
ALTER index IF EXISTS index_116_02 RENAME TO index_116_02;
select relname from pg_class where relname like 'index_116%' order by relname;
--已存在
ALTER index IF EXISTS index_116_02 RENAME TO index_116_01;
select relname from pg_class where relname like 'index_116%' order by relname;
ALTER index IF EXISTS index_116_01 RENAME TO index_116;
select relname from pg_class where relname like 'index_116%' order by relname;
ALTER index IF EXISTS index_116_02 RENAME TO index_116_01;
select relname from pg_class where relname like 'index_116%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_116 CASCADE;