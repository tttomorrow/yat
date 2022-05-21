-- @testpoint: 创建list分区表不支持的功能DELTAROW_THRESHOLD合理报错

--step1:创建分区表with (DELTAROW_THRESHOLD = 555)expect失败
drop table if exists t_partition_list_0029;
create table t_partition_list_0029(p_id int,p_name varchar,p_age int)
with (DELTAROW_THRESHOLD = 555)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

