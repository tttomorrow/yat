-- @testpoint: Hash分区表结合 with 子句（FILLFACTOR）有效值

--step1：创建hash分区表结合fillfactor=10 expect：成功
drop table if exists t_partition_hash_0063_01;
create table t_partition_hash_0063_01
(id                         number(7),
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  )with(fillfactor=10)
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功插入一条数据
insert into t_partition_hash_0063_01 values(1,'李','李四','数学老师');

--step3：创建hash分区表结合fillfactor=100 expect：成功
drop table if exists t_partition_hash_0063_02;
create table t_partition_hash_0063_02
(id                         number(7),
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  )with(fillfactor=100)
partition by hash(id)
(partition p1,
 partition p2);

--step4：插入数据 expect：成功插入一条数据
insert into t_partition_hash_0063_02 values(1,'李','李四','数学老师');

--step5：创建hash分区表结合fillfactor=11 expect：成功
drop table if exists t_partition_hash_0063_03;
create table t_partition_hash_0063_03
(id                         number(7),
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  )with(fillfactor=11)
partition by hash(id)
(partition p1,
 partition p2);

--step6：插入数据 expect：成功插入一条数据
insert into t_partition_hash_0063_03 values(1,'李','李四','数学老师');

--step7：创建hash分区表结合fillfactor=99 expect：成功
drop table if exists t_partition_hash_0063_04;
create table t_partition_hash_0063_04
(id                         number(7),
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  )with(fillfactor=99)
partition by hash(id)
(partition p1,
 partition p2);

--step8：插入数据 expect：成功插入一条数据
insert into t_partition_hash_0063_04 values(1,'李','李四','数学老师');

--step9：清理环境 expect：成功
drop table if exists t_partition_hash_0063_01;
drop table if exists t_partition_hash_0063_02;
drop table if exists t_partition_hash_0063_03;
drop table if exists t_partition_hash_0063_04;