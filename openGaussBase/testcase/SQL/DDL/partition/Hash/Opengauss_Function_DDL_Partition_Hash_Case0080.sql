-- @testpoint: Hash分区表中truncate分区

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0080_01;
create table t_partition_hash_0080_01(
id int,
name varchar(100),
age int)
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入四条数据
insert into t_partition_hash_0080_01 values( 1,  '张三', 25);
insert into t_partition_hash_0080_01 values( 2,  '张三', 26);
insert into t_partition_hash_0080_01 values( 3,  '张三', 27);
insert into t_partition_hash_0080_01 values( 4,  '张三', 28);

--step3：查看p1分区数据 expect：p1分区中包含两条数据
select * from t_partition_hash_0080_01 partition (p1);

--step4：truncate p1分区 expect：truncate p1分区成功
alter table t_partition_hash_0080_01 truncate partition p1;

--step5：查看分区数据 expect：p1分区数据为零
select * from t_partition_hash_0080_01 partition (p1);

--step6：清理环境 expect：成功
drop table if exists t_partition_hash_0080_01;