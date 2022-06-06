-- @testpoint: 值存储的长度转换

--建表
drop table if exists test_cast_0027 cascade;
create table test_cast_0027(c_varchar char(20));

--查询转换计划
--test point：长度需要转换:success
explain performance insert into test_cast_0027 values('abcdef');
SELECT c_varchar,octet_length(c_varchar) FROM test_cast_0027;

--testpoint：长度不需要转换:success
explain performance insert into test_cast_0027 values('12345678901234567890');
SELECT c_varchar,octet_length(c_varchar) FROM test_cast_0027;

--清理环境
drop table if exists test_cast_0027 cascade;