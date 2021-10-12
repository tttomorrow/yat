-- @testpoint: 插入数值0
-- @modified at: 2020-11-13

drop table if exists test_clob_049;
create table test_clob_049(c_clob clob);
insert into test_clob_049 values(0);
select * from test_clob_049;
drop table test_clob_049;