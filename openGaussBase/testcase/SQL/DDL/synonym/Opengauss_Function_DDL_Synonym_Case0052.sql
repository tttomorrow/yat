-- @testpoint: 创建同义词，有多个对象名，合理报错
-- @modify at: 2020-11-25
--建表
drop table if exists test_SYN_052;
drop table if exists test_SYN_052_bak;
create table test_SYN_052(a int);
create table test_SYN_052_bak(a int);
--创建同义词,报错
drop synonym if exists SYN_052;
create synonym SYN_052 for test_SYN_052,test_SYN_052_bak;
--清理环境
drop table if exists test_SYN_052;
drop table if exists test_SYN_052_bak;