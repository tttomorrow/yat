-- @testpoint: DQL语法，覆盖特殊字符

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,'~~');
insert into test_clob values(2,'@@');
insert into test_clob values(3,'￥%');
insert into test_clob values(4,'&*&');

select * from test_clob where c_clob='~~';
select * from test_clob where c_clob='@@';
select * from test_clob where c_clob='￥%';
select * from test_clob where c_clob='&*&';

drop table test_clob;