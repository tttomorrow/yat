-- @testpoint: 测试创建哈希索引时，是否支持NULL first|last关键字，部分step合理报错

--创建表
drop table if exists t_hash_index_0060;
create table t_hash_index_0060
(
    id01 char(20),
    id02 char(20)
) 
with(orientation=row);

--创建哈希索引(是否支持nulls first|last)
create index i_hash_index_0060_01 on t_hash_index_0060 using hash(id01 nulls first);
create index i_hash_index_0060_02 on t_hash_index_0060 using hash(id02 nulls last);

--删除哈希索引
drop index if exists i_hash_index_0060_01;
drop index if exists i_hash_index_0060_02;

--删除表、表空间
drop table t_hash_index_0060 cascade;
