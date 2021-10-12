-- @testpoint: join on条件后使用
drop table if exists test_limit_009;
create table test_limit_009 ("LIMIT" int,id int);
insert into test_limit_009 values (-999,1);
insert into test_limit_009 values (-10000,2);
insert into test_limit_009 values (-10000,3);
insert into test_limit_009 values (100,3);
insert into test_limit_009 values (100,2);
drop table if exists test_limit_011;
create table test_limit_011 ("LIMIT" int,id int);
insert into test_limit_011 values (-999,9);
insert into test_limit_011 values (1,10);
insert into test_limit_011 values (2,11);
commit;
select t1.id  from test_limit_011 t1 inner join test_limit_009 t2 on t1."LIMIT" = t2."LIMIT" order by t1.id;
--清理环境
drop table if exists test_limit_009;
drop table if exists test_limit_011;