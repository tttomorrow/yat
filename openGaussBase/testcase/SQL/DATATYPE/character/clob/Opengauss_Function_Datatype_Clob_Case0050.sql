-- @testpoint: 插入正常值
-- @modified at: 2020-11-13

drop table if exists test_clob_050;
create table test_clob_050(c_clob clob);
insert into test_clob_050 values('ffffffffffffffefqwefqfqwefqweqw');
select * from test_clob_050;
drop table test_clob_050;