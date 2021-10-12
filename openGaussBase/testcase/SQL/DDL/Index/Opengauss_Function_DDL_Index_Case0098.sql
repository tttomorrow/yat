--  @testpoint: TABLESPACE：不存在的表空间

DROP TABLE if EXISTS test_index_table_098 CASCADE;
create table test_index_table_098(
c_float1 float
) WITH (ORIENTATION = row);

--建索引
drop index if exists index_098_01;
--不存在的表空间
create index index_098_01 on test_index_table_098 using btree(c_float1)  TABLESPACE test_space_notexist where c_float1 >50;
--建表空间又删除
drop tablespace if exists test_space_01;
CREATE TABLESPACE test_space_01 RELATIVE LOCATION 'tablespace/tablespace_1';
drop tablespace if exists test_space_01;
create index index_098_01 on test_index_table_098 using btree(c_float1)  TABLESPACE test_space_01 where c_float1 >50;
select relname from pg_class where relname like 'index_098_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_098 CASCADE;
