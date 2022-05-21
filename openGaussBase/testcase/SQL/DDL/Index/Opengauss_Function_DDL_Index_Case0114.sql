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
ALTER index IF EXISTS a RENAME TO a12345678901234567890123456789012345678901234567890123456789012;
select relname from pg_class where relname ='a12345678901234567890123456789012345678901234567890123456789012';
ALTER index IF EXISTS a12345678901234567890123456789012345678901234567890123456789012 RENAME TO index_114_$;
select relname from pg_class where relname ='index_114_$';
--清理环境
DROP TABLE if EXISTS test_index_table_114 CASCADE;