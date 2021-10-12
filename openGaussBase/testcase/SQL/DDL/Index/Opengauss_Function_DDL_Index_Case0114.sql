--  @testpoint:RENAME TO：修改索引名称1-63位

--创建表
DROP TABLE if EXISTS test_index_table_114 CASCADE;
create table test_index_table_114(
c_int int
) WITH (ORIENTATION = row) ;

--无if exists 合理报错
ALTER index index_114 RENAME TO a;
ALTER index if exists index_114 RENAME TO a;
--建索引
drop index if exists index_114;
create index index_114 on test_index_table_114(c_int);
select relname from pg_class where relname like 'index_114%' order by relname;

--rename
ALTER index IF EXISTS index_114 RENAME TO a;
select relname from pg_class where relname ='a';
select relname from pg_class where relname ='index_114_$';
--清理环境
DROP TABLE if EXISTS test_index_table_114 CASCADE;