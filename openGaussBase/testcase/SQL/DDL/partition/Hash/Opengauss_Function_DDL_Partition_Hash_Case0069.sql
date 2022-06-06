-- @testpoint: Hash分区表结合关键字COMPRESS 合理报错

--step1：创建hash分区表 expect：合理报错
drop table if exists t_partition_hash_0069_01;
create table t_partition_hash_0069_01(
id int,
name varchar(100),
age int
)compress
partition by hash(id)
(partition p1,
 partition p2);