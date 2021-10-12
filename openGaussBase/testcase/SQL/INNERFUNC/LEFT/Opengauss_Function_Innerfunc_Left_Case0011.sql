-- @testpoint:  update的使用
drop table if exists test_left;
create table test_left(a int,b varchar2(20));
insert into test_left values(1,'xiexiaoyu');
insert into test_left values(2,'llllll');
insert into test_left values(3,'vvvvvv');
update test_left set B='888' where LEFT(B,4) = 'xiex';
select A,B from test_left order by A;
drop table if exists test_left;