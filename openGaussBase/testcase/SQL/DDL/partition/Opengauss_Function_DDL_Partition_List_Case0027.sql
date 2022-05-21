-- @testpoint: 修改分区键字段类型，合理报错

--step1:创建list分区表;expect:成功
drop table if exists t_partition_list_0027;
create table t_partition_list_0027(p_id int,p_name varchar,p_bit bit(3))
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

--step2:修改分区键数据类型;expect:合理报错
alter table t_partition_list_0027 modify p_id char;

--step3:清理环境,expect成功
drop table t_partition_list_0027;



