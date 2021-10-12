-- @testpoint: 在Range分区表上创建了本地和全局分区索引后，exchange时指定verbose

--step1:建表造数据; expect:成功
create table t_partition_0072_01 (a int, b int);
insert into t_partition_0072_01 select 100 from generate_series(1, 100);
insert into t_partition_0072_01 select 200 from generate_series(1, 200);
insert into t_partition_0072_01 select 300 from generate_series(1, 200);
insert into t_partition_0072_01 select 400 from generate_series(1, 200);
insert into t_partition_0072_01 select 500 from generate_series(1, 200);
create index local_exchange_table_index1 on t_partition_0072_01(a);
create table t_partition_0072_02 (a int, b int)
partition by range(a)
(
partition p1 values less than (200),
partition p2 values less than (300),
partition p3 values less than (400),
partition p4 values less than (500),
partition p5 values less than (600)
);
create index local_alter_table_index1 on t_partition_0072_02(a) local;
create index global_alter_table_index1 on t_partition_0072_02(b) global;

--step2:alter exchange verbose; expect:成功
alter table t_partition_0072_02 exchange partition (p1) with table t_partition_0072_01 verbose update global index;
select count(*) from t_partition_0072_01;
select count(*) from t_partition_0072_02;

--step3:清理环境; expect:成功
drop table t_partition_0072_01;
drop table t_partition_0072_02;