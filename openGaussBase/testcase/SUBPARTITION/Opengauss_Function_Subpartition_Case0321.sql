-- @testpoint: range_hash二级分区表：分区键0个空/字符串空,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0321;
drop tablespace if exists ts_subpartition_0321;
create tablespace ts_subpartition_0321 relative location 'subpartition_tablespace/subpartition_tablespace_0321';

--step2: 创建二级分区表,二级分区键为null; expect:合理报错
create table if not exists t_subpartition_0321
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0321
partition by range (col_1) subpartition by hash ( )
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
    subpartition t_subpartition_0321
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 创建二级分区表,二级分区键“”; expect:合理报错
drop table if exists t_subpartition_0321;
create table if not exists t_subpartition_0321
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0321
partition by range (col_1) subpartition by hash ("")
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
    subpartition t_subpartition_0321
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step4: 创建二级分区表,一级分区键二级分区键都为空; expect:合理报错
drop table if exists t_subpartition_0321;
create table if not exists t_subpartition_0321
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0321
partition by range () subpartition by hash ()
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
    subpartition t_subpartition_0321
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0321;
drop tablespace if exists ts_subpartition_0321;