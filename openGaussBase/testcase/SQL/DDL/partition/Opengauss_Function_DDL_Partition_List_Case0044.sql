-- @testpoint: 插入与分区键数据类型不一致的数据,合理报错

--step1:创建list分区;expect:成功
drop table if exists t_partition_list_0044;
create table t_partition_list_0044(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10));

--step2:插入数据;expect:合理报错
insert into t_partition_list_0044  values ('wang','wang',20);

--step3:清理环境;expect:成功
drop table t_partition_list_0044;

