-- @testpoint: range_hash二级分区表：列存表/压缩,测试点合理报错

--step1: 创建表空间; expect:成功

--test1: 列存表with ( {storage_parameter = value} [, ... ] ) ]
--step2: 创建二级分区列存表; expect:合理报错
drop table if exists t_subpartition_00316;
create table if not exists t_subpartition_0316
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
with(orientation = column)
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
--step3: 创建二级分区列存表,压缩; expect:合理报错
drop table if exists t_subpartition_00316;
create table if not exists t_subpartition_0316
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
with(orientation = column,compression=middle)
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

--test2: compress
--step4: 创建二级分区表,压缩; expect:合理报错
drop table if exists t_subpartition_00316;
create table if not exists t_subpartition_0316
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)compress
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

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0316;