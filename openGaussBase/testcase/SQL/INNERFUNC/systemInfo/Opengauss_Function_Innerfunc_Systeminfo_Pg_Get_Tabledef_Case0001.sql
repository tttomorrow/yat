-- @testpoint: pg_get_tabledef函数根据table_name获取表定义
drop table if exists table_test;
create table table_test(a varchar);
select pg_get_tabledef('table_test');
drop table if exists table_test;