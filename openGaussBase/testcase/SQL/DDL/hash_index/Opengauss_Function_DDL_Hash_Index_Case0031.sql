-- @testpoint: 测试索引存在与否对修改哈希索引的影响，部分step合理报错

--创建表
drop table if exists  t_hash_index_0031;
create table t_hash_index_0031(id01 float(4),id02 int) with(orientation=row);

--创建哈希索引
create index i_hash_index_0031_01 on t_hash_index_0031 using hash(id01);

--修改哈希索引(索引存在)
alter index  i_hash_index_0031_01 rename to i_hash_index_0031_03;
--修改哈希索引(索引不存在)
alter index  i_hash_index_0031_02 rename to i_hash_index_0031_04;

--删除哈希索引
drop index i_hash_index_0031_03;
drop index i_hash_index_0031_04;

--删除表、表空间
drop table  t_hash_index_0031 cascade;