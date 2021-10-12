-- @testpoint: 关键字limit作为普通表的列名在update语句的使用
drop table if exists test_limit_004;
create table test_limit_004 ("LIMIT" int);
insert into test_limit_004 values (1);
commit;
select "LIMIT" from test_limit_004 order by "LIMIT";
update test_limit_004 set "LIMIT" = 2;
commit;
--清理环境
drop table if exists test_limit_004;