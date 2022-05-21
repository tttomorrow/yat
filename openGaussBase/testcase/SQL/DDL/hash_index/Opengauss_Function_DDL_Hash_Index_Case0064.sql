-- @testpoint: 测试创建哈希索引时，是否支持fastupdate，部分step合理报错

--创建表
drop table if exists t_hash_index_0064;
create table t_hash_index_0064
(
    id01 varchar,
    id02 char(20) not null
) 
with(orientation=row);

--创建哈希索引(是否支持fastupdate)
create index i_hash_index_0064_01 on t_hash_index_0064 using hash(id01) with(FASTUPDATE=on);
create index i_hash_index_0064_02 on t_hash_index_0064 using hash(id02) with(FASTUPDATE=off);

--删除哈希索引
drop index if exists i_hash_index_0064_01;
drop index if exists i_hash_index_0064_02;

--删除表、表空间
drop table t_hash_index_0064 cascade;
