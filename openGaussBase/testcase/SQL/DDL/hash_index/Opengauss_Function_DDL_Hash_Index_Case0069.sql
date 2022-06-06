-- @testpoint: 测试创建哈希索引，是否支持排序，部分step合理报错

--创建表
drop table if exists t_hash_index_0069;
create table t_hash_index_0069
(
    id01 char(20),
    id02 char(20)
) 
with(orientation=row);

--创建哈希索引(是否支持ASC|DESC)
create index i_hash_index_0069_01 on t_hash_index_0069 using hash(id01 asc);
create index i_hash_index_0069_02 on t_hash_index_0069 using hash(id02 desc);

--删除哈希索引
drop index if exists i_hash_index_0069_01;
drop index if exists i_hash_index_0069_02;

--删除表、表空间
drop table t_hash_index_0069 cascade;
