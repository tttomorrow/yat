--  @testpoint:关键字limit作为临时表的列名在update语句的使用
drop table if exists test_temporary_limit_004;
create temporary table test_temporary_limit_004("limit" int);
insert into test_temporary_limit_004 values (1);
commit;
select "limit" from test_temporary_limit_004 order by "limit";
update test_temporary_limit_004 set "LIMIT" = 2;
commit;
select "LIMIT" from test_temporary_limit_004 order by "LIMIT";