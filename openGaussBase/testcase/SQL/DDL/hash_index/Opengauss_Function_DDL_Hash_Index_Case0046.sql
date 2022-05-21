-- @testpoint: 测试表名存在与否对重建哈希索引的影响，部分step合理报错

--创建表
drop table if exists t_hash_index_0046;
create table t_hash_index_0046(id01 varchar,id02 int) with(orientation=row);

--创建哈希索引
create index i_hash_index_0046_01 on t_hash_index_0046 using hash(id01);

--重建（表名存在）
reindex table t_hash_index_0046_01;

--重建（表名不存在）
reindex table i_hash_index_0046_02;

--删除索引
drop index i_hash_index_0046_01;

--删除表、表空间
drop table t_hash_index_0046 cascade;
