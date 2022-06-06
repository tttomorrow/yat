-- @testpoint: 测试在列存表中创建哈希索引时是否支持单字段与多字段以及同一字段创建多个哈希索引,同时测试宽窄表，部分step合理报错

--创建表
drop table if exists t_hash_index_0058_01;
create table t_hash_index_0058_01(id01 int, id02 int) with(orientation=row);
drop table if exists t_hash_index_0058_02;
create table t_hash_index_0058_02(id03 int, id04 int) with(orientation=row);
drop table if exists t_hash_index_0058_03;
create table t_hash_index_0058_03(id05 int,id06 int,id07 int,id08 int,id09 int,id10 int,id11 int,id12 int,id13 int,id14 int,id15 int,id16 int,id17 int,id18 int) with(orientation=row);


--创建哈希索引(单字段)
create index i_hash_index_0058_01 on t_hash_index_0058_01 using hash(id01);
create index i_hash_index_0058_02 on t_hash_index_0058_01 using hash(id01);

--创建哈希索引(多字段)
create index i_hash_index_0058_03 on t_hash_index_0058_02 using hash(id03,id04);

--创建哈希索引（宽表）
create index i_hash_index_0058_04 on t_hash_index_0058_03 using hash(id03);

--删除哈希索引
drop index if exists i_hash_index_0058_01;
drop index if exists i_hash_index_0058_02;
drop index if exists i_hash_index_0058_03;
drop index if exists i_hash_index_0058_04;

--删除表、表空间
drop table t_hash_index_0058_01 cascade;
drop table t_hash_index_0058_02 cascade;
drop table t_hash_index_0058_03 cascade;
