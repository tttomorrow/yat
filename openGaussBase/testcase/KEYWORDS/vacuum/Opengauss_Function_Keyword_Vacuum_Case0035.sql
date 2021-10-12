-- @testpoint: vacuum内存清理，验证功能正常

drop table if exists vacuum_test_01;
create table vacuum_test_01(id_src int,name_src varchar(10));
drop index if exists vacuum_index_01;
create unique index vacuum_index_01 on vacuum_test_01(id_src);

vacuum (verbose,analyse) vacuum_test_01;
drop table if exists vacuum_test_01;