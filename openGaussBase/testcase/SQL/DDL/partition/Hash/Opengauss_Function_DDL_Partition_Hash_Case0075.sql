-- @testpoint: Hash分区表中插入新的字段

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0075_01;
create table t_partition_hash_0075_01(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0075_01 values( 1,  '张三', 25);
insert into t_partition_hash_0075_01 values( 2,  '张三', 25);

--step3：插入字段 expect：成功插入新的字段job
alter table t_partition_hash_0075_01 add column job varchar(10);

--step4：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0075_01 values( 3,  '李四', 25, 'teacher');
insert into t_partition_hash_0075_01 values( 4,  '王五', 25, 'student');

--step5：查看各分区数据 expect：各分区分别有两条数据
select * from t_partition_hash_0075_01 partition (p1);
select * from t_partition_hash_0075_01 partition (p2);

--step6：清理环境 expect：成功
drop table if exists t_partition_hash_0075_01;