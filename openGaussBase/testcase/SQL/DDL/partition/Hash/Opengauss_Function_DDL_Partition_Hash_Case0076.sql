-- @testpoint: Hash分区表中删除字段

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0076_01;
create table t_partition_hash_0076_01(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0076_01 values( 1,  '张三', 25);
insert into t_partition_hash_0076_01 values( 2,  '张三', 25);

--step3：删除字段 expect：成功删除字段age
alter table t_partition_hash_0076_01 drop column if exists age;

--step4：查看分区数据 expect：p2分区有两条数据p1分区无数据
select * from t_partition_hash_0076_01 partition (p1);
select * from t_partition_hash_0076_01 partition (p2);

--step5：清理环境 expect：成功
drop table if exists t_partition_hash_0076_01;