-- @testpoint: 测试哈希索引是否支持重命名索引分区

--创建表
drop table if exists t_hash_index_0036;
create table t_hash_index_0036(id01 float(4),id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than('g'),
    partition p02 values less than('n'),
    partition p03 values less than('z')
);
--创建哈希索引
create index i_hash_index_0036 on t_hash_index_0036 using hash(id02) local
(
    partition index_p01,
    partition index_p02,
    partition index_p03
);

--修改哈希索引(重命名索引分区)
alter index i_hash_index_0036 rename partition index_p01 to index_p00;

--删除哈希索引
drop index i_hash_index_0036;

--删除表、表空间；
drop table t_hash_index_0036 cascade;