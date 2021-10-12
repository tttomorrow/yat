--  @testpoint:关键字limit加引号作为临时表的列名
drop table if exists test_temporary_limit_001;

create temporary table test_temporary_limit_001("limit" int);