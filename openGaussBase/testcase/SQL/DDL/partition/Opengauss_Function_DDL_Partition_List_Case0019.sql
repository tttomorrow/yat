-- @testpoint: list分区表，不支持的功能 COMPRESSION，合理报错

--step1:创建list分区表 with (COMPRESSION=LOW)，expect失败
drop table if exists t_partition_list_0019;
create table t_partition_list_0019(p_id int,p_name varchar,p_age int)
with (COMPRESSION=LOW)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));
