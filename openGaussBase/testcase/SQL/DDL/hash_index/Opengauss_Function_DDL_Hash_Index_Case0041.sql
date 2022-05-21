-- @testpoint: 测试在concurrently关键字下，能否同时删除多个哈希索引，部分step合理报错

--创建表
drop table if exists t_hash_index_0041;
create table t_hash_index_0041(id01 int,id02 char(30),id03 float(4),id04 varchar) with (orientation=row);

--创建哈希索引
create index i_hash_index_0041_01 on t_hash_index_0041 using hash(id01);
create index i_hash_index_0041_02 on t_hash_index_0041 using hash(id02);
create index i_hash_index_0041_03 on t_hash_index_0041 using hash(id03);
create index i_hash_index_0041_04 on t_hash_index_0041 using hash(id04);
--删除哈希索引(多索引)
drop index concurrently i_hash_index_0041_01, i_hash_index_0041_02;

--删除哈希索引(单索引)
drop index concurrently i_hash_index_0041_03;
drop index concurrently i_hash_index_0041_04;

--删除索引
drop index if exists i_hash_index_0041_01;
drop index if exists i_hash_index_0041_02;
drop index if exists i_hash_index_0041_03;
drop index if exists i_hash_index_0041_04;

--删除表、表空间
drop table t_hash_index_0041 cascade;
