-- @testpoint: 分区个数为1时删除分区,合理报错

--step1:创建list分区表， 分区个数为1个,expect成功
drop table if exists  t_partition_list_0021;
create table t_partition_list_0021(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10));

--step2:删除唯一分区,expect失败
alter table t_partition_list_0021 drop partition p1;

--step3:清理环境，expect成功
drop table t_partition_list_0021;

