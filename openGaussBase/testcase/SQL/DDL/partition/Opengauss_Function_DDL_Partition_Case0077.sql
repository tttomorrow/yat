-- @testpoint: 在Range分区表上创建本地和全局分区索引后，exchange时指定verbose

--step1:创建普通表; expect:成功
drop table if exists t_partition_0077_01;
create table t_partition_0077_01 (a int, b int);

--step2:插入数据; expect:成功
insert into t_partition_0077_01 select 100 from generate_series(1, 100);
insert into t_partition_0077_01 select 200 from generate_series(1, 200);
insert into t_partition_0077_01 select 300 from generate_series(1, 200);

--step3:创建索引; expect:成功
create index i_partition_0077_01 on t_partition_0077_01(a);

--step4:创建范围分区表; expect:成功
create table t_partition_0077_02 (a int, b int)
partition by range(a)
(partition p1 values less than (200),
 partition p2 values less than (300),
 partition p3 values less than (400),
 partition p4 values less than (500),
 partition p5 values less than (600));

--step5:创建分区表本地和全局索引; expect:成功
create index i_partition_0077_02 on t_partition_0077_02(a) local;
create index i_partition_0077_03 on t_partition_0077_02(b) global;

--step6:修改分区，exchange时指定verbose; expect:成功
alter table t_partition_0077_02 exchange partition (p1) with table t_partition_0077_01 verbose update global index;

--step7:查看数据; expect:成功
select count(*) from t_partition_0077_01;
select count(*) from t_partition_0077_02;

--step8:清理环境; expect:成功
drop table t_partition_0077_01 cascade;
drop table t_partition_0077_02 cascade;
