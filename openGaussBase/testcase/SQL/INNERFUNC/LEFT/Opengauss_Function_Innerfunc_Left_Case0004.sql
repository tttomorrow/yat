-- @testpoint:  where条件
drop table if exists test_left;
create table test_left(a int,b int);
insert into test_left values(0,1);
insert into test_left values(1,4);
insert into test_left values(2,2);
select * from test_left where LEFT('xiexiaoyu', 4)='xiex' order by a;
drop table if exists test_left;