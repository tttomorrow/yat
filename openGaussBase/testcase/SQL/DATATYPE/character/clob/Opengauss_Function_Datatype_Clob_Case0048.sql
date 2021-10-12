-- @testpoint: 插入合理值，结合条件查询
-- @modified at: 2020-11-13

drop table if exists test_clob_048;
create table test_clob_048(c_clob clob);
insert into test_clob_048 values('a'),('中国'),('国a'),('abcd'),('asd');
select * from test_clob_048 where c_clob between 'a' and '中国a' order by 1;
select * from test_clob_048 where c_clob like 'abc%' order by c_clob;
drop table test_clob_048;
