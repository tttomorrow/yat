-- @testpoint: DQL语法，与like结合

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,'abcd');
insert into test_clob values(2,'abcde');
insert into test_clob values(3,'abcdefg');
insert into test_clob values(4,'sdfgfhjj');

select * from test_clob where c_clob like 'abc%' order by 1;

drop table test_clob;
