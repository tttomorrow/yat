-- @testpoint: having条件
drop table if exists test_left;
create table test_left(a int,b int);
insert into test_left values(0,1);
insert into test_left values(1,4);
insert into test_left values(2,2);
select sum(a),b from test_left group by b having LEFT('xiexiaoyu', 4)='xiex' order by b;
drop table if exists test_left;