--  @testpoint: create index CONCURRENTLY：指定多个索引名:合理报错

--建普通表
DROP TABLE if EXISTS test_index_table_191 CASCADE;
create table test_index_table_191(
c_int int);

--建索引
drop index if exists index_191_01;
drop index if exists index_191_02;
create index CONCURRENTLY index_191_01,index_191_02 on test_index_table_191(c_int) ;

--清理环境
DROP TABLE if EXISTS test_index_table_191 CASCADE;