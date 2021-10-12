-- @testpoint: pg_get_tabledef函数根据oid获取表定义
drop table if exists table_test;
create table table_test(a varchar);
select pg_get_tabledef(oid) from PG_CLASS where relname='table_test';
drop table if exists table_test;