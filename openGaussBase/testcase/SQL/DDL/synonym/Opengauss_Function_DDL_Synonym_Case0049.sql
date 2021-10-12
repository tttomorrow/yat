-- @testpoint: 创建同义词后删除同义词对象，查询同义词，合理报错
-- @modify at: 2020-11-25
--建表
drop table if exists test_SYN_049 cascade;
create table test_SYN_049(a int);
--创建同义词
drop synonym if exists SYN_049;
create synonym SYN_049 for test_SYN_049;
--删表
drop table test_SYN_049;
--查询同义词，报错
select * from SYN_049;
--删除同义词
drop synonym if exists SYN_049;