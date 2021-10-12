-- @testpoint: 关键字limit作为普通表的列名在delete语句的使用 部分测试点合理报错
drop table if exists test_limit_005;
create table test_limit_005 ("LIMIT" int);
insert into test_limit_005 values (1);
commit;
select "LIMIT" from test_limit_005 order by "LIMIT";
delete from test_limit_005 where "LIMIT" = 1;
select LIMIT from test_limit_005 order by "LIMIT";
--清理环境
drop table if exists test_limit_005;