-- @testpoint: List分区表与普通表交换数据（普通表含唯一索引）合理报错

--step1:创建list分区表;expect:成功
drop table if exists t_partition_list_0064;
create table t_partition_list_0064(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

--step2:创建唯一索引;expect:成功
create unique index p_unique_idx on t_partition_list_0064(p_age);

--step3:插入数据;expect:成功
insert into t_partition_list_0064 values( 10,  '张三', 25);
insert into t_partition_list_0064 values( 10,  '张三', 26);
insert into t_partition_list_0064 values( 20,  '张三', 27);
insert into t_partition_list_0064 values( 20,  '张三', 28);

--step4:创建普通表;expect:成功
drop table if exists exchange_tab;
create table exchange_tab(
p_id int,
p_name varchar,
p_age int);

--step5:创建唯一索引;expect:成功
create unique index ex_unique_idx on exchange_tab(p_age);

--step6:交换数据;expect:合理报错
alter table t_partition_list_0064 exchange partition (p1) with table exchange_tab;

--step7:清理环境;expect:成功
drop index p_unique_idx;
drop index ex_unique_idx;
drop table if exists t_partition_list_0064;
drop table if exists exchange_tab;


