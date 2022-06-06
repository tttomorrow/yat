-- @testpoint: 测试新名称命名正确与否对修改哈希索引的影响，部分step合理报错

--创建表
drop table if exists t_hash_index_0033;
create table t_hash_index_0033(id01 int,id02 char) with (orientation=row);

--创建哈希索引
create index i_hash_index_0033_01 on t_hash_index_0033 using hash(id01);
create index i_hash_index_0033_02 on t_hash_index_0033 using hash(id02);

--修改哈希索引(新名称为字符串)
alter index if exists i_hash_index_0033_01 rename to i_hash_index_0033_03;
--修改哈希索引(新名称不为字符串)
alter index if exists i_hash_index_0033_02 rename to 123456;

--删除哈希索引
drop index i_hash_index_0033_01;
drop index i_hash_index_0033_02;
drop index i_hash_index_0033_03;

--删除表、表空间
drop table t_hash_index_0033 cascade;