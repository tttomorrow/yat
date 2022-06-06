-- @testpoint: Hash分区表结合（foreign key）match full

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0082_01;
create table if not exists t_partition_hash_0082_01
(id         number(7) primary key,
name        varchar2(20))
partition by hash(id)
(partition p1,
 partition p2);

 --step2：结合（foreign key）match full参数创建hash分区表 expect：成功
drop table if exists t_partition_hash_0082_02;
create table if not exists t_partition_hash_0082_02
(id         number(7) primary key,
name        varchar2(20),
foreign key(id) references t_partition_hash_0082_01(id) match full)
partition by hash(id)
(partition p1,
 partition p2);

--step3：插入数据 expect：t_partition_hash_0082_01表中成功插入两条数据
insert into t_partition_hash_0082_01 values(1,'张三');
insert into t_partition_hash_0082_01 values(2,'李四');

--step4：插入数据 expect：t_partition_hash_0082_02表中成功插入两条数据
insert into t_partition_hash_0082_02 values(1,'张三');
insert into t_partition_hash_0082_02 values(2,'李四');

--step5：查看数据 expect：t_partition_hash_0082_01表中包含两条数据
select * from t_partition_hash_0082_01;

--step6：查看数据 expect：t_partition_hash_0082_02表中包含两条数据
select * from t_partition_hash_0082_02;

--step7：清理环境 expect：成功
drop table if exists t_partition_hash_0082_02;
drop table if exists t_partition_hash_0082_01;