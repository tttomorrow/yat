-- @testpoint: Hash分区表结合LIKE INCLUDING  ALL参数 合理报错

--step1：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0062_01;
create table t_partition_hash_0062_01
(id                         number(7) constraint t_partition_hash_0062_01_id_nn not null,
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入两条数据
insert into t_partition_hash_0062_01 values(1,'李','李四','数学老师');
insert into t_partition_hash_0062_01 values(2,'王','王五','化学老师');

--step3：查看数据表 expect：成功展示step2中插入的两条数据
select * from t_partition_hash_0062_01;

--step4：结合like all参数建表 expect：合理报错
create table t_partition_hash_0062_02 (like  t_partition_hash_0062_01  including all);

--step5：清理环境 expect：成功
drop table if exists t_partition_hash_0062_02;
drop table if exists t_partition_hash_0062_01;