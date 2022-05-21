-- @testpoint: Hash分区表结合关键字 row movement

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0071_01;
create table t_partition_hash_0071_01(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2)
enable row movement;

 --step2：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0071_01 values(1,'李四');
insert into t_partition_hash_0071_01 values(2,'王五');

--step3：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0071_02;
create table t_partition_hash_0071_02(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2)
disable row movement;

 --step4：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0071_02 values(1,'李四');
insert into t_partition_hash_0071_02 values(2,'王五');

--step5：查询数据 expect：表中成功展示step2中插入的两条数据
select * from t_partition_hash_0071_01;

--step6：查询数据 expect：表中成功展示step4中插入的两条数据
select * from t_partition_hash_0071_02;

--step7：清理环境 expect：成功
drop table if exists t_partition_hash_0071_01;
drop table if exists t_partition_hash_0071_02;