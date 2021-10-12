-- @testpoint: where条件中使用
drop table if exists test_limit_009;
create table test_limit_009 ("LIMIT" int,id int);
insert into test_limit_009 values (-999,1);
insert into test_limit_009 values (-10000,2);
insert into test_limit_009 values (-10000,3);
insert into test_limit_009 values (100,3);
insert into test_limit_009 values (100,2);
select "LIMIT" from test_limit_009 where abs("LIMIT") = 999;
--清理环境
drop table if exists test_limit_009;
