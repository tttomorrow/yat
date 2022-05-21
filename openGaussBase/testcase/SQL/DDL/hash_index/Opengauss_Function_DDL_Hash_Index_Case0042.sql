-- @testpoint: 测试在concurrently关键字下，添加CASCADE能否正确删除哈希索引，部分step合理报错

--创建表
drop table if exists t_hash_index_0042;
create table t_hash_index_0042(id01 int,id02 char(30),id03 float(4),id04 varchar) with (orientation=row);

--创建哈希索引
create index i_hash_index_0042_01 on t_hash_index_0042 using hash(id01);
create index i_hash_index_0042_02 on t_hash_index_0042 using hash(id02);

--删除哈希索引(添加cascade)
drop index concurrently i_hash_index_0042_01 cascade;
--删除哈希索引(未添加cascade)
drop index concurrently i_hash_index_0042_02;

--删除索引
drop index if exists i_hash_index_0042_01;
drop index if exists i_hash_index_0042_02;

--删除表、表空间
drop table t_hash_index_0042 cascade;