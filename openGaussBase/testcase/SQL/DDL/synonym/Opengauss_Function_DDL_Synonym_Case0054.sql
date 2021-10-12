-- @testpoint: 在同义词上创建视图,依赖对象删除后，查询同义词，合理报错
-- @modify at: 2020-11-25
--创建表
drop table if exists test_SYN_054;
create table test_SYN_054 (a int);
--插入数据
insert into test_SYN_054 values(1),(2),(3),(4);
--创建同义词
drop synonym if exists SYN_054;
create synonym SYN_054 for test_SYN_054;
--查询
select * from SYN_054;
--创建视图
drop view if exists v_SYN_054 ;
create view v_SYN_054 as select * from SYN_054;
--查询视图
select * from v_SYN_054;
--删除表
drop table test_SYN_054 cascade;
--查同义词和视图：报错
select * from SYN_054;
select * from v_SYN_054;
--重新创建表
drop table if exists test_SYN_054 ; 
create table test_SYN_054(a int,b char(1));
--查同义词，成功
select * from SYN_054;
--查视图，报错
select * from v_SYN_054;
--清空环境
drop table test_SYN_054;
drop view if exists v_SYN_054;
drop synonym SYN_054;