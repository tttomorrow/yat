-- @testpoint: truncate分区

--step1:.创建list分区表;expect:成功
drop table if exists t_partition_list_0050;
create table t_partition_list_0050(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--step2:插入数据;expect:成功
insert into t_partition_list_0050 values (10,'wangke',18);
insert into t_partition_list_0050 values (20,'wangke',18);
insert into t_partition_list_0050 values (30,'wangke',18);

--step3:truncate分区part_2;expect:成功
alter table t_partition_list_0050 truncate partition  part_2;

--step4:查看分区2信息;expect:成功
select * from t_partition_list_0050 partition (part_2);

--step3:清理环境;expect:成功
drop table t_partition_list_0050;

