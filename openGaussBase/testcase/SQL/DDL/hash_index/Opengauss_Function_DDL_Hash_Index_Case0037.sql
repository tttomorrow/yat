-- @testpoint: 测试修改哈希索引分区索引名时，旧分区索引名存在与否的影响，部分step合理报错

--创建分区表
drop table if exists t_hash_index_0037;
create table t_hash_index_0037(id01 float(4),id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than('g'),
    partition p02 values less than('n'),
    partition p03 values less than('z')
);
--创建哈希索引
create index i_hash_index_0037 on t_hash_index_0037 using hash(id02) local
(
    partition index_p01,
    partition index_p02,
    partition index_p03
);

--修改哈希索引(旧分区索引名存在)
alter index i_hash_index_0037 rename partition index_p01 to index_p00;

--修改哈希索引(旧分区索引名不存在)
alter index i_hash_index_0037 rename partition index_p11 to index_p00;

--删除哈希索引
drop index i_hash_index_0037;

--删除表、表空间；
drop table t_hash_index_0037 cascade;
