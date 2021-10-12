-- @testpoint:  count的使用
drop table if exists test_left;
create table test_left(a int,b char(20));
insert into test_left values(1,'xiexiaoyu');
insert into test_left values(2,'llllll');
insert into test_left values(3,'vvvvvv');
insert into test_left values(4,'llllll');
select count(1) from test_left where LEFT(B,4) = 'llll';
drop table if exists test_left;