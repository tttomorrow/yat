-- @testpoint: 在同义词上创建同义词成功，但是查询时，合理报错
-- @modify at: 2020-11-25
--建表
drop table if exists test_SYN_055;
create table test_SYN_055 (a int);
--创建同义词
create or replace synonym test_SYN_055_1 for test_SYN_055;
drop synonym if exists test_SYN_055_2;
create synonym test_SYN_055_2 for test_SYN_055_1;
--查询
select * from test_SYN_055_1;
--查询，报错
select * from test_SYN_055_2;
--清空环境
drop table test_SYN_055 cascade;
drop synonym test_SYN_055_1;
drop synonym test_SYN_055_2;