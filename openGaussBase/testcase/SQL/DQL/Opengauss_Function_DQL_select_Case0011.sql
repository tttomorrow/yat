-- @testpoint: DQL语法，结合order by后跟clob列

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,'abcdeee');
insert into test_clob values(2,'abcd');
insert into test_clob values(3,'abc');
insert into test_clob values(4,'bcdefg');
insert into test_clob values(5,'中国abc');
insert into test_clob values(6,'abc中国');

select * from test_clob where c_clob like 'abc%' order by c_clob;

drop table test_clob;