--  @testpoint: column_name：1列多种索引:success
--建表行存
DROP TABLE if EXISTS test_index_table_080 CASCADE;
create table test_index_table_080(id int,name text);

drop index if exists index_080_01;
drop index if exists index_080_02;
drop index if exists index_080_03;
create index index_080_01 on test_index_table_080(id);
create index index_080_02 on test_index_table_080 using gin(to_tsvector('english', id));
--合理报错
create index index_080_03 on test_index_table_080 using gist(id);
--查询
select relname from pg_class where relname like '%index_080_%' order by relname asc;


--建表列存
DROP TABLE if EXISTS test_index_table_080 CASCADE;
create table test_index_table_080(id int,name text) WITH (ORIENTATION = column);

drop index if exists index_080_01;
drop index if exists index_080_02;
drop index if exists index_080_03;
create index index_080_01 on test_index_table_080(id);
create index index_080_02 on test_index_table_080 using btree(id);
create index index_080_03 on test_index_table_080 using gin(to_tsvector('english', id));
--查询
select relname from pg_class where relname like '%index_080_%' order by relname asc;

--清理数据
DROP TABLE if EXISTS test_index_table_080 CASCADE;