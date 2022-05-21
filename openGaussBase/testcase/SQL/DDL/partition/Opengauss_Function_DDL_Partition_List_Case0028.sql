-- @testpoint: list分区表，不支持的功能 MAX_BATCHROW，合理报错

--step1:创建分区表(with MAX_BATCHROW=10000）expect失败
drop table if exists t_partition_list_0028;
create table t_partition_list_0028(p_id int,p_name varchar,p_age int)
with (MAX_BATCHROW=10000)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

