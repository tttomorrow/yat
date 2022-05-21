-- @testpoint: Hash分区表结合 with 子句（FILLFACTOR）无效值 合理报错

--step1：创建hash分区表 expect：fillfactor为无效值合理报错
drop table if exists t_partition_hash_0067_01;
create table t_partition_hash_0067_01
(id                         number(7),
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  )with(fillfactor=9)
partition by hash(id)
(partition p1,
 partition p2);

--step2：创建hash分区表 expect：fillfactor为无效值合理报错
drop table if exists t_partition_hash_0067_02;
create table t_partition_hash_0067_02
(id                         number(7),
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  )with(fillfactor=101)
partition by hash(id)
(partition p1,
 partition p2);