-- @testpoint: 关键字all作为临时表的列名
drop table if exists test_temporary_all_001;
create temporary table test_temporary_all_001("all" int);
drop table if exists test_temporary_all_001;
