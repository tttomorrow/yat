-- @testpoint: 测试能否正确删除哈希索引，部分step合理报错

--创建表
drop table if exists t_hash_index_0040;
create table t_hash_index_0040(id01 int,id02 int) with(orientation=row);

--创建哈希索引
create index i_hash_index_0040_01 on t_hash_index_0040 using hash(id01);

--删除哈希索引(存在)
drop index i_hash_index_0040_01;
--删除哈希索引(不存在)
drop index i_hash_index_0040_02;

--删除表、表空间
drop table t_hash_index_0040 cascade;