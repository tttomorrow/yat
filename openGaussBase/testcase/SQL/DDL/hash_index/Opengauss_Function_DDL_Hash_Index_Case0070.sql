-- @testpoint: 测试create index unique关键字是否支持哈希索引，部分step合理报错

--创建普通行存表
drop table if exists t_hash_index_0070;
create table t_hash_index_0070(id01 varchar,id02 int) with(orientation=row);

--索引名重复
create index i_hash_index_0070_01 on t_hash_index_0070 using hash(id01);
create unique index i_hash_index_0070_01 on t_hash_index_0070 using hash(id01);

 
--索引名未重复
create index i_hash_index_0070_02 on t_hash_index_0070 using hash(id02);
drop index i_hash_index_0070_02;
create unique index i_hash_index_0070_02 on t_hash_index_0070 using hash(id02);


--删除索引
drop index if exists i_hash_index_0070_01;
drop index if exists i_hash_index_0070_02;


--删除表、表空间        
drop table t_hash_index_0070 cascade;
