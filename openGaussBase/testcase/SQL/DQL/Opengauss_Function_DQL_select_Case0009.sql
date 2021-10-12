-- @testpoint: DQL语法，与is not null结合

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,'abcd');
insert into test_clob values(2,'abcde');
insert into test_clob values(3,'bcdefg');
insert into test_clob values(4,'中国abc');

select * from test_clob where c_clob is not null and c_clob between 'a' and '中国a' and exists(select c_clob from test_clob where c_clob between 'a' and '中国a' ) order by 1;

drop table test_clob;