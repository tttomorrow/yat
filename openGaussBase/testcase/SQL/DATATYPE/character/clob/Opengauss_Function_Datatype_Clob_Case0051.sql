-- @testpoint: 插入负数测试
-- @modified at: 2020-11-13

drop table if exists test_clob_051;
create table test_clob_051(c_clob clob);
insert into test_clob_051 values(-123456);
select * from test_clob_051;
drop table if exists test_clob_051;