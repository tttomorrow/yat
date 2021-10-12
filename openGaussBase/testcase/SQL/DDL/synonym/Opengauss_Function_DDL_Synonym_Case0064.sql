-- @testpoint: 使用explain语句，查询同义词
-- @modify at: 2020-11-26
--建表
drop table if EXISTS test_SYN_064 cascade;
create table test_SYN_064(a int,b varchar);
insert into test_SYN_064 values(1,'a');
--创建表的同义词
drop synonym if EXISTS SYN_064 cascade;
create synonym SYN_064 for test_SYN_064;
--查询
explain select * from SYN_064;
--清理环境
drop table if EXISTS test_SYN_064 cascade;
drop synonym if EXISTS SYN_064 cascade;