-- @testpoint: 插入空值
-- @modified at: 2020-11-13

drop table if exists test_clob_054;
create table test_clob_054(c_clob clob);
insert into test_clob_054 values('');
insert into test_clob_054 values(null);
select * from test_clob_054;
drop table test_clob_054;
