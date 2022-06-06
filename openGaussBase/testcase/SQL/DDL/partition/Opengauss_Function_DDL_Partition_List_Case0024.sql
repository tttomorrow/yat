-- @testpoint: 参数填充因子为100

--step1:创建分区表填充因子为100，expect成功
drop table if exists t_partition_list_0024;
create table t_partition_list_0024(p_id int,p_name varchar,p_age int)
with (fillfactor = 100)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--step2:清理环境，expect成功
drop table t_partition_list_0024;

