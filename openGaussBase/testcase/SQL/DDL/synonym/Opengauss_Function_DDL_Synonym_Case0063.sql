-- @testpoint: 创建索引同义词：创建不报错，查询时，合理报错
--建表
drop table if EXISTS test_SYN_063 cascade;
create table test_SYN_063(a int,b varchar);
--创建索引
drop index if exists test_syn_index063;
CREATE UNIQUE INDEX test_syn_index063 ON test_SYN_063(b);
--创建同义词
drop SYNONYM if exists syn_063;
create SYNONYM syn_063 for test_syn_index063;
--查询
select * from syn_063;
--清理环境
drop table if EXISTS test_SYN_063 cascade;
drop SYNONYM if exists syn_index;
drop SYNONYM if exists syn_063;