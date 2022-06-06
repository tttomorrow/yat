-- @testpoint: List分区表与普通表交换数据（对应信息不一致）合理报错

--step1:创建list分区表;expect:成功
drop table if exists t_partition_list_0062;
create table t_partition_list_0062(
id int,
name varchar(100),
age int)
partition by list(id)
(partition p1 values(10),
 partition p2 values(20));

--step2:插入数据;expect:成功
insert into t_partition_list_0062 values( 10,  '张三', 25);
insert into t_partition_list_0062 values( 10,  '张三', 26);
insert into t_partition_list_0062 values( 20,  '张三', 27);
insert into t_partition_list_0062 values( 20,  '张三', 28);

--step3:建普通表;expect:成功
drop table if exists exchange_tab;
create table exchange_tab(
id int,
age int);

--step4:插入数据;expect:成功
insert into exchange_tab values( 10,25);
insert into exchange_tab values( 10,26);

--step5:交换数据;expect:合理报错
alter table t_partition_list_0062 exchange partition (p1) with table exchange_tab;

--step6:清理环境;expect:成功
drop table if exists t_partition_list_0062;
drop table if exists exchange_tab;
