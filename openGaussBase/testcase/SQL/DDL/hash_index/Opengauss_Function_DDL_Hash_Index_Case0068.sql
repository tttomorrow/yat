-- @testpoint: 测试创建哈希索引时，分区表名存在与否的影响，部分step合理报错

--创建表空间
drop tablespace if exists ts_hash_index_0068_01;
create tablespace ts_hash_index_0068_01 relative location 'tablespace/partspace01';
drop tablespace if exists ts_hash_index_0068_02;
create tablespace ts_hash_index_0068_02 relative location 'tablespace/partspace02';
drop tablespace if exists ts_hash_index_0068_03;
create tablespace ts_hash_index_0068_03 relative location 'tablespace/partspace03';
drop tablespace if exists ts_hash_index_0068_04;
create tablespace ts_hash_index_0068_04 relative location 'tablespace/partspace04';
--创建表
drop table if exists t_hash_index_0068;
create table t_hash_index_0068(id01 char(20),id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than ('g'),
    partition p02 values less than ('n') tablespace ts_hash_index_0068_01,
    partition p03 values less than ('z') tablespace ts_hash_index_0068_02
);

--创建分区哈希索引
--分区表名存在
create index i_hash_index_0068_01 on t_hash_index_0068 using hash(id02) local
(
    partition index_p01,
    partition index_p02 tablespace ts_hash_index_0068_03,
    partition index_p03 tablespace ts_hash_index_0068_04
);
--分区表名不存在
create index i_hash_index_0068_02 on t_hash_index_0068 using hash(id02) local
(
    partition index_p01,
    partition index_p02 tablespace row_part_ts_hash_index_0068_01,
    partition index_p03 tablespace row_part_ts_hash_index_0068_02
);
--删除哈希索引
drop index i_hash_index_0068_01 cascade;
drop index if exists i_hash_index_0068_02 cascade;

--删除表、表空间
drop table t_hash_index_0068 cascade;
drop tablespace ts_hash_index_0068_01;
drop tablespace ts_hash_index_0068_02;
drop tablespace ts_hash_index_0068_03;
drop tablespace ts_hash_index_0068_04;