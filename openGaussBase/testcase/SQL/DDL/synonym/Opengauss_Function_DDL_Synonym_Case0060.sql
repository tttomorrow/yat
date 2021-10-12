-- @testpoint: 创建的同义词存在相同的视图名或者表名
--创建表
drop table if exists test_SYN_060 cascade;
drop table if exists test_SYN_060_2 cascade;
create table test_SYN_060(a int);
create table test_SYN_060_2(b int);
--创建视图
create or replace VIEW  v_SYN_060 as select * from test_SYN_060;
--创建与表名相同的同义词
drop synonym if exists test_SYN_060;
create synonym test_SYN_060 for test_SYN_060_2;
--创建与视图名相同的同义词
drop synonym if exists v_SYN_060;
create synonym v_SYN_060 for test_SYN_060_2;
--查询
SELECT * from test_SYN_060;
SELECT * from v_SYN_060;
--数据清理
drop table test_SYN_060 cascade;
drop table test_SYN_060_2 cascade;
drop synonym if exists test_SYN_060;
drop synonym if exists v_SYN_060;