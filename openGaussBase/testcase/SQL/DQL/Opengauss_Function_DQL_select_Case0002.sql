-- @testpoint: DQL语法，结合中文

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,'你好');
insert into test_clob values(2,'我是');
insert into test_clob values(3,'中国人');
insert into test_clob values(4,'我爱中国');

select * from test_clob where c_clob='我是';
select * from test_clob where c_clob='中国人';
select * from test_clob where c_clob='我爱中国';

drop table test_clob;

