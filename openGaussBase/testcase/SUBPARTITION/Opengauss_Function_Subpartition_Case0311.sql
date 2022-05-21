-- @testpoint: range_hash二级分区表：create if not exists不同名/不同schema

--test1: 不同名
--step1: 创建普通表; expect:成功
drop table if exists  t_subpartition_0311;
create table if not exists t_subpartition_0311
(
    col_1 int ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int  generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
);
--step2: 创建不同名二级分区表; expect:成功
drop table if exists  t_subpartition_0311_01;
create table if not exists t_subpartition_0311
(
    col_1 int ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int  generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--test2: 不同schema
--step3: 创建新schema; expect:成功
drop schema if exists s_subpartition_0311 cascade;
create schema s_subpartition_0311;
--step4: 创建和普通表同名不同schema二级分区表; expect:成功
create table if not exists s_subpartition_0311.t_subpartition_0311
(
    col_1 int ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int  generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step5: 创建和二级分区表同名不同schema二级分区表; expect:成功
create table if not exists s_subpartition_0311.t_subpartition_0311
(
    col_1 int ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int  generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step6: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0311
(
    col_1 int ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int  generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step7: 清理环境; expect:成功
drop table if exists t_subpartition_0311;
drop table if exists t_subpartition_0311_01;
drop schema if exists s_subpartition_0311 cascade;