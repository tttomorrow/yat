--  @testpoint:关键字limit作为临时表的列名在delete语句的使用
drop table if exists test_temporary_limit_005;
create temporary table test_temporary_limit_005("limit" int);
insert into test_temporary_limit_005 values (1);
commit;
select "limit" from test_temporary_limit_005 order by "limit";
update test_temporary_limit_005 set "LIMIT" = 2;
commit;
select "LIMIT" from test_temporary_limit_005 order by "LIMIT";
delete from test_temporary_limit_005 where "LIMIT" = 2;
select "LIMIT" from test_temporary_limit_005 order by "LIMIT";