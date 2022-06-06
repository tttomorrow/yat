-- @testpoint: 测试表空间名存在与否对修改哈希索引的影响，部分step合理报错

--创建表空间
drop tablespace if exists ts_hash_index_0034_01;
create tablespace ts_hash_index_0034_01 relative location 'tablespace/row_space01';
drop tablespace if exists ts_hash_index_0034_02;
create tablespace ts_hash_index_0034_02 relative location 'tablespace/row_space02';
--创建表
drop table if exists t_hash_index_0034;
create table t_hash_index_0034(id01 int,id02 float(4)) with (orientation=row);

--创建哈希索引
create index i_hash_index_0034_01 on t_hash_index_0034 using hash(id01);
create index i_hash_index_0034_02 on t_hash_index_0034 using hash(id02);

--修改哈希索引(表空间名存在)
alter index i_hash_index_0034_01 set tablespace ts_hash_index_0034_02;
--修改哈希索引(表空间名不存在)
alter index i_hash_index_0034_02 set tablespace ts_hash_index_0034_03;

--删除哈希索引
drop index i_hash_index_0034_01;
drop index i_hash_index_0034_02;

--删除表、表空间
drop table t_hash_index_0034 cascade;
drop tablespace ts_hash_index_0034_01;
drop tablespace ts_hash_index_0034_02;

