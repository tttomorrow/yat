-- @testpoint: 测试create index concurrently关键字是否支持在列存表、分区表、临时表上创建哈希索引，部分step合理报错

--创建表
drop table if exists t_hash_index_0052_01;
create table t_hash_index_0052_01(id01 float(4), id02 int) with(orientation=column);
drop table if exists t_hash_index_0052_02;
create table t_hash_index_0052_02(id03 int,id04 char) with(orientation=row)  
partition by range(id04)
(
    partition p01 values less than ('g'),
    partition p02 values less than ('n'),
    partition p03 values less than ('z')
);
create temporary table t_hash_index_0052_03(id05 int, id06 float(4)) with(orientation=row);

--创建哈希索引(列存表)
create index concurrently i_hash_index_0052_01 on t_hash_index_0052_01 using hash(id01);
--创建哈希索引(分区表)
create index concurrently i_hash_index_0052_02 on t_hash_index_0052_02 using hash(id04) local;
--创建哈希索引(临时表)
create index concurrently i_hash_index_0052_03 on t_hash_index_0052_03 using hash(id06);

--删除哈希索引
drop index if exists i_hash_index_0052_01;
drop index if exists i_hash_index_0052_02;
drop index if exists i_hash_index_0052_03;

--删除表、表空间
drop table t_hash_index_0052_01 cascade;
drop table t_hash_index_0052_02 cascade;
drop table t_hash_index_0052_03 cascade;
