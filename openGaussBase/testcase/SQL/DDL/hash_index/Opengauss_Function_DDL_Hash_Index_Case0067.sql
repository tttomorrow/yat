-- @testpoint: 测试创建分区哈希索引时，分区索引命名规范与否的影响，部分step合理报错

--创建表
drop table if exists t_hash_index_0067;
create table t_hash_index_0067(id01 char(20),id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than ('g'),
    partition p02 values less than ('n'),
    partition p03 values less than ('z')
);

--创建分区哈希索引
create index i_hash_index_0067_01 on t_hash_index_0067 using hash(id02) local
(
    partition index_p01,
    partition index_p02,
    partition 132415646598
);
create index i_hash_index_0067_02 on t_hash_index_0067 using hash(id02) local
(
    partition index_p01,
    partition index_p02,
    partition index_p03
);

--删除哈希索引
drop index if exists i_hash_index_0067_01 cascade;
drop index if exists i_hash_index_0067_02 cascade;

--删除表、表空间
drop table t_hash_index_0067 cascade;