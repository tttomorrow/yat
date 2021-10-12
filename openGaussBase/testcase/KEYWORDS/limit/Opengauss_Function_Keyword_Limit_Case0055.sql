-- @testpoint: 与函数结合使用（参数为表的列--limit）
drop table if exists test_limit_009;
create table test_limit_009 ("LIMIT" int,id int);
insert into test_limit_009 values (-999,1);
insert into test_limit_009 values (-10000,2);
insert into test_limit_009 values (-10000,3);
insert into test_limit_009 values (100,3);
insert into test_limit_009 values (100,2);
commit;
select abs("LIMIT") t1 from test_limit_009 order by t1;
--清理环境
drop table if exists test_limit_009;
