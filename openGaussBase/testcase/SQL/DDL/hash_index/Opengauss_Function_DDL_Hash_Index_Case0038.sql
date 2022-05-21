-- @testpoint: 测试修改索引分区的所属表空间时，表空间存在与否的影响，部分step合理报错

--创建表空间
drop tablespace if exists ts_hash_index_0038_01;
create tablespace ts_hash_index_0038_01 relative location 'tablespace/row_space01';
drop tablespace if exists ts_hash_index_0038_02;
create tablespace ts_hash_index_0038_02 relative location 'tablespace/row_space02';

--创建分区表
drop table if exists t_hash_index_0038;
create table t_hash_index_0038(id01 float(4),id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than('g'),
    partition p02 values less than('n'),
    partition p03 values less than('z')
);

--创建分区哈希索引
create index i_hash_index_0038 on t_hash_index_0038 using hash(id02) local
(
    partition index_p01,
    partition index_p02,
    partition index_p03
);

--修改修改索引分区的所属表空间(新表空间存在)
alter index i_hash_index_0038 move partition index_p01 tablespace ts_hash_index_0038_02;

--修改修改索引分区的所属表空间(新表空间不存在)
alter index i_hash_index_0038 move partition index_p01 tablespace ts_hash_index_0038_03;

--删除分区哈希索引
drop index i_hash_index_0038;

--删除表、表空间
drop table t_hash_index_0038 cascade;
drop tablespace ts_hash_index_0038_01;
drop tablespace ts_hash_index_0038_02;