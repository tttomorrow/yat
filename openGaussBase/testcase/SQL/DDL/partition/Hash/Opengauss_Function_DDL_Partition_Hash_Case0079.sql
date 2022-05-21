-- @testpoint: Hash分区表与普通表交换数据（普通表含唯一索引）合理报错

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0079_01;
create table t_partition_hash_0079_01(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2);

--step2：分区表创建唯一索引 expect：创建唯一索引成功
create unique index p_unique_idx on t_partition_hash_0079_01(age);

--step3：插入数据 expect：成功插入四条数据
insert into t_partition_hash_0079_01 values( 1,  '张三', 25);
insert into t_partition_hash_0079_01 values( 2,  '张三', 26);
insert into t_partition_hash_0079_01 values( 3,  '张三', 27);
insert into t_partition_hash_0079_01 values( 4,  '张三', 28);

--step4：创建普通表 expect：成功
drop table if exists t_partition_hash_0079_02;
create table t_partition_hash_0079_02(
id int,
name varchar(100),
age int);

--step5：普通表创建唯一索引 expect：创建唯一索引成功
create unique index ex_unique_idx on t_partition_hash_0079_02(age);

--step6：交换数据 expect：合理报错
alter table t_partition_hash_0079_01 exchange partition (p1) with table t_partition_hash_0079_02;

--step7：清理环境 expect：成功
drop index p_unique_idx;
drop index ex_unique_idx;
drop table if exists t_partition_hash_0079_01;
drop table if exists t_partition_hash_0079_02;