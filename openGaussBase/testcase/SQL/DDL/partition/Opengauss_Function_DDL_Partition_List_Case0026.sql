-- @testpoint: 参数填充因子为10.5合理报错

--step1:创建分区表填充因子为10.5，expect失败
drop table if exists t_partition_list_0026;
create table t_partition_list_0026(p_id int,p_name varchar,p_age int)
with (fillfactor = 10.5)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));


