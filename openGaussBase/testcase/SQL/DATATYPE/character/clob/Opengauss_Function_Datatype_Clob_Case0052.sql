-- @testpoint: 插入布尔值
-- @modified at: 2020-11-13

drop table if exists test_clob_052;
create table test_clob_052(c_clob clob);
insert into test_clob_052 values(true),(false),('yes'),('no');
select * from test_clob_052;
drop table test_clob_052;