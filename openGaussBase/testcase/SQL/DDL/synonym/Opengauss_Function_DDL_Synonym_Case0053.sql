-- @testpoint: 创建的同义词与表名相同
-- @modify at: 2020-11-25
--建表
drop table if exists test_SYN_053 cascade;
create table test_SYN_053 (a int);
--创建同义词
drop synonym if exists test_SYN_053;
CREATE synonym test_SYN_053 for test_SYN_053;
--查询
select * from test_SYN_053;
--清空环境
drop table if exists test_SYN_053 cascade;
drop synonym if exists test_SYN_053;