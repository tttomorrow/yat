-- @testpoint: unkonw类型存为目标类型

--建表
drop table if exists test_cast_0025 cascade;
create table test_cast_0025(c_int int);

--查询转换计划
--test point：unkonw类型存为目标类型：success
explain performance insert into test_cast_0025 values('25');

--清理环境
drop table if exists test_cast_0025 cascade;