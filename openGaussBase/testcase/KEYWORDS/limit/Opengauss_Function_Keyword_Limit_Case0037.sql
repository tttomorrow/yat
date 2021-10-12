-- @testpoint: 关键字limit作为普通表的列名在insert语句的使用
drop table if exists test_limit_002;
create table test_limit_002 ("LIMIT" int);
insert into test_limit_002 values (1);
commit;
select "LIMIT" from test_limit_002 order by "LIMIT";
--清理环境
drop table if exists test_limit_002;
