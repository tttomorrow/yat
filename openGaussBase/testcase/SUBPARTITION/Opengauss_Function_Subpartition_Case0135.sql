-- @testpoint: list_hash二级分区表：create if not exists不同名/不同schema

--test1: 不同名
--step1: 创建普通表; expect:成功
drop table if exists  t_subpartition_0135;
create  table if not exists t_subpartition_0135
(
  col_1 int ,
  col_2 int not null ,
    col_3 varchar2 ( 30 ) not null ,
  col_4 int generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
);
--step2: 创建不同名普通表; expect:成功
drop table if exists  t_subpartition_0135_01;
create  table if not exists t_subpartition_0135_01
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
);
--step3: 创建不同名二级分区表; expect:成功
drop table if exists  t_subpartition_0135_01;
create  table if not exists t_subpartition_0135_01
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition p_hash_1_3
 ),
 partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
 (
  subpartition p_hash_2_1 ,
  subpartition p_hash_2_2 ,
  subpartition p_hash_2_3 ,
  subpartition p_hash_2_4 ,
  subpartition p_hash_2_5
 ),
 partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
 partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
 (
  subpartition p_hash_4_1
 ),
 partition p_list_5 values (default)
 (
  subpartition p_hash_5_1
 ),
 partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
 (
  subpartition p_hash_6_1 ,
  subpartition p_hash_6_2 ,
  subpartition p_hash_6_3
 )
) enable row movement ;

--test2: 不同schema
--step4: 创建新schema; expect:成功
drop schema if exists s_subpartition_0135 cascade;
create schema s_subpartition_0135;
--step5: 创建和普通表同名不同schema二级分区表; expect:成功
create  table if not exists s_subpartition_0135.t_subpartition_0135
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition p_hash_1_3
 ),
 partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
 (
  subpartition p_hash_2_1 ,
  subpartition p_hash_2_2 ,
  subpartition p_hash_2_3 ,
  subpartition p_hash_2_4 ,
  subpartition p_hash_2_5
 ),
 partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
 partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
 (
  subpartition p_hash_4_1
 ),
 partition p_list_5 values (default)
 (
  subpartition p_hash_5_1
 ),
 partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
 (
  subpartition p_hash_6_1 ,
  subpartition p_hash_6_2 ,
  subpartition p_hash_6_3
 )
) enable row movement ;

--step6: 创建和二级分区表同名不同schema二级分区表; expect:成功
create  table if not exists s_subpartition_0135.t_subpartition_0135_01
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition p_hash_1_3
 ),
 partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
 (
  subpartition p_hash_2_1 ,
  subpartition p_hash_2_2 ,
  subpartition p_hash_2_3 ,
  subpartition p_hash_2_4 ,
  subpartition p_hash_2_5
 ),
 partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
 partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
 (
  subpartition p_hash_4_1
 ),
 partition p_list_5 values (default)
 (
  subpartition p_hash_5_1
 ),
 partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
 (
  subpartition p_hash_6_1 ,
  subpartition p_hash_6_2 ,
  subpartition p_hash_6_3
 )
) enable row movement ;

--step31:创建二级分区表; expect:成功
create  table if not exists t_subpartition_0135
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
with(fillfactor=80)
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition p_hash_1_3
 ),
 partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
 (
  subpartition p_hash_2_1 ,
  subpartition p_hash_2_2 ,
  subpartition p_hash_2_3 ,
  subpartition p_hash_2_4 ,
  subpartition p_hash_2_5
 ),
 partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
 partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
 (
  subpartition p_hash_4_1
 ),
 partition p_list_5 values (default)
 (
  subpartition p_hash_5_1
 ),
 partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
 (
  subpartition p_hash_6_1 ,
  subpartition p_hash_6_2 ,
  subpartition p_hash_6_3
 )
) enable row movement ;

--step7: 清理环境; expect:成功
drop table if exists t_subpartition_0135;
drop table if exists t_subpartition_0135_01;
drop schema if exists s_subpartition_0135 cascade;