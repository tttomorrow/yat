-- @testpoint: 创建不同类型的二级分区表

--step1: 创建range_list二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1' ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '1' ),
    subpartition p_list_2_2 values ( default )
  )
) enable row movement;
--step2: 创建range_hash二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 ,
    subpartition p_list_1_2
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 ,
    subpartition p_list_2_2
  )
) enable row movement;
--step3: 创建range_range二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  primary key,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int  generated always as(2*col_2) stored ,
    check (col_4 >= col_2)
)
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step4: 创建list_list二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_list_1_1 values ( 5,6,7,8,9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_list_2_1 values ( 15,16,17,18,19 ),
    subpartition p_list_2_2 values ( default )
  )
);
--step5: 创建list_range二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by list (col_1) subpartition by range (col_2)
(
  partition p_list_1 values(1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_list_1_1 values less than( 5 ),
    subpartition p_list_1_2 values less than( 10 )
  ),
  partition p_list_2 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_list_2_1 values less than( 15 ),
    subpartition p_list_2_2 values less than( maxvalue )
  )
);
--step6: 创建list_hash二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_list_1_1 ,
    subpartition p_list_1_2
  ),
  partition p_list_2 values (11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_list_2_1 ,
    subpartition p_list_2_2
  )
) ;
--step7: 创建hash_list二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by hash (col_1) subpartition by list (col_2)
(
  partition p_hash_1
  (
    subpartition p_hash_1_1 values (1,2,3,4,5,6,7,8,9,10 ),
    subpartition p_hash_1_2 values (default )
  ),
  partition p_hash_2
  (
    subpartition p_hash_2_1 values (1,2,3,4,5 ),
    subpartition p_hash_2_2 values (6,7,8,9,10 )
  )
);
--step8: 创建hash_hash二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by hash (col_1) subpartition by hash (col_2)
(
  partition p_hash_1
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2
  ),
  partition p_hash_2
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2
  )
);
--step9: 创建hash_range二级分区表; expect:成功
drop table if exists t_subpartition_0074;
create table t_subpartition_0074
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by hash (col_1) subpartition by range (col_2)
(
  partition p_hash_1
  (
    subpartition p_hash_1_1 values less than(10 ),
    subpartition p_hash_1_2 values less than(maxvalue )
  ),
  partition p_hash_2
  (
    subpartition p_hash_2_1 values less than(5 ),
    subpartition p_hash_2_2 values less than(10 )
  )
) enable row movement;

--step10: 删除二级分区表; expect:成功
drop table if exists t_subpartition_0074;