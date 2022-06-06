-- @testpoint: 测试哈希索引是否支持重建分区索引

--创建分区表
drop table if exists t_hash_index_0039;
create table t_hash_index_0039(id01 int,id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than('g'),
    partition p02 values less than('n'),
    partition p03 values less than('z')
);

--创建哈希索引
create index i_hash_index_0039 on t_hash_index_0039 using hash(id01) local
(
    partition index_p01,
    partition index_p02,
    partition index_p03
);

--修改哈希索引(重建分区索引)
alter index i_hash_index_0039 rebuild partition index_p01;

--删除哈希索引
drop index i_hash_index_0039;

--删除表
drop table t_hash_index_0039 cascade;

