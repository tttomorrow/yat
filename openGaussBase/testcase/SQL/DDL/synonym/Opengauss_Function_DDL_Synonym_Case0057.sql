-- @testpoint: 通过表创建同义词；通过同义词创建视图；再通过视图创建同义词；通过同义词创建视图
-- @modify at: 2020-11-25
--创建表
drop table if exists test_SYN_057 cascade;
create table test_SYN_057(a int);
--插入数据
insert into test_SYN_057 values(1),(2);
--创建同义词
drop synonym if exists SYN_057;
create synonym SYN_057 for test_SYN_057;
--查询
SELECT * from SYN_057;
--通过同义词创建视图
drop view if exists v_SYN_057;
create or replace view v_SYN_057 as select * from SYN_057;
--查询
select * from v_SYN_057;
--给视图创建同义词
drop synonym if exists v_SYN_057_1;
create synonym v_SYN_057_1 for v_SYN_057;
--查询
select * from v_SYN_057_1;
--在同义词基础上创建视图
drop view if exists v_SYN_057_2;
create or replace view v_SYN_057_2 as select * from v_SYN_057_1;
--通过视图查询
select * from v_SYN_057_2;
--清理环境
drop table if exists test_SYN_057 cascade;
drop synonym if exists SYN_057;
drop synonym if exists v_SYN_057_1;
