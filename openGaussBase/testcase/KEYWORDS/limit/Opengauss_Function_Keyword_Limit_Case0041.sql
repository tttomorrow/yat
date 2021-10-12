--  @testpoint:关键字limit作为临时表的列名在insert语句的使用
drop table if exists test_temporary_limit_002;
create temporary table test_temporary_limit_002("limit" int);
insert into test_temporary_limit_002 values (1);
commit;
select "limit" from test_temporary_limit_002 order by "limit";