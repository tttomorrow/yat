--  @testpoint:在线创建索引

--建普通表
DROP TABLE if EXISTS test_index_table_178 CASCADE;
create table test_index_table_178(
c_int int);

drop index if exists index_178_01;
create index concurrently index_178_01 on test_index_table_178(c_int);
select relname from pg_class where relname like 'index_178_%';

explain select c_int from test_index_table_178 where c_int > 50 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_178 CASCADE;
