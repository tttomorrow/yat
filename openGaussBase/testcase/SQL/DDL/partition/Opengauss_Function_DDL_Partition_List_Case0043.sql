-- @testpoint: 创建list分区表，验证分区表支持的数据类型（位串类型），验证分区键不支持的数据类型（位串类型），部分测试点合理报错

--step1:创建list分区表，支持的数据类型bit(3);expect:成功
drop table if exists t_partition_list_0042_01;
create table t_partition_list_0042_01(p_id int,p_name varchar,p_bit bit(3))
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

--step2:创建分区表，分区键不支持的数据类型bit(3);expect:合理报错
drop table if exists t_partition_list_0042_02;
create table t_partition_list_0042_02(p_id int,p_name varchar,p_bit bit(3))
partition by list(p_cidr)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

--step3：清理环境;expect:成功
drop table if exists t_partition_list_0042_01;

