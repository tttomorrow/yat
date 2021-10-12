-- @testpoint: case when条件中使用limit列名
drop table if exists test_limit_009;
create table test_limit_009 ("LIMIT" int,id int);
insert into test_limit_009 values (-999,1);
insert into test_limit_009 values (-10000,2);
insert into test_limit_009 values (-10000,3);
insert into test_limit_009 values (100,3);
insert into test_limit_009 values (100,2);
select id,(case when "LIMIT" <> -999 then 'a' else 'b' end) t1 from test_limit_009 order by id,t1;
--清理环境
drop table if exists test_limit_009;