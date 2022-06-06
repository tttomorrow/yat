-- @testpoint: 测试索引名存在与否对重建哈希索引的影响，部分step合理报错

--创建普通行存表
drop table if exists t_hash_index_0045;
create table t_hash_index_0045(id01 int,id02 int) with(orientation=row);

--创建哈希索引
create index i_hash_index_0045_01 on t_hash_index_0045 using hash(id01);

--重建（索引名存在）
reindex index i_hash_index_0045_01;

--重建（索引名不存在）
reindex index i_hash_index_0045_02;

--删除索引
drop index i_hash_index_0045;

--删除表、表空间.
drop table t_hash_index_0045 cascade;
