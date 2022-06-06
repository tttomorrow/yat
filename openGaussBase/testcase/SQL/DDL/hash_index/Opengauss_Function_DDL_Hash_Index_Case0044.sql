-- @testpoint: 测试在没有concurrently关键字下，是否支持CASCADE和restrict关键字

--创建表
drop table if exists t_hash_index_0044;
create table t_hash_index_0044(id01 int,id02 float(4)) with (orientation=row);

--创建哈希索引
create index i_hash_index_0044_01 on t_hash_index_0044 using hash(id01);
create index i_hash_index_0044_02 on t_hash_index_0044 using hash(id02);

--删除哈希索引(是否支持CASCADE|RESTRICT)
drop index i_hash_index_0044_01 cascade;
drop index i_hash_index_0044_02 restrict;

--删除表、表空间
drop table t_hash_index_0044 cascade;