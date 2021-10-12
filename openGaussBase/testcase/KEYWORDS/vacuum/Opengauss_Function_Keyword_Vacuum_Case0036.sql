-- @testpoint: 在事务中执行vacuum内存清理，不能成功（合理报错）

start transaction;
drop table if exists vacuum_test_02;
create table vacuum_test_02(id_src int,name_src varchar(10));
drop index if exists vacuum_index_02;
create unique index vacuum_index_02 on vacuum_test(id_src);
vacuum (verbose,analyse) vacuum_test;
commit;
drop table if exists vacuum_test_02;