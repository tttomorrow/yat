-- @testpoint: range_range二级分区表：分区键0个空/字符串空,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0271;
drop tablespace if exists ts_subpartition_0271;
create tablespace ts_subpartition_0271 relative location 'subpartition_tablespace/subpartition_tablespace_0271';

--step2: 创建二级分区表,二级分区键为null; expect:合理报错
create   table if not exists t_subpartition_0271
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0271
partition by range (col_1) subpartition by range (null)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition t_subpartition_0271 values less than( 10 )
  )
) enable row movement;
--step3: 创建二级分区表,二级分区键0个; expect:合理报错
drop table if exists t_subpartition_0271;
create   table if not exists t_subpartition_0271
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0271
partition by range (col_1) subpartition by range ( )
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition t_subpartition_0271 values less than( 10 )
  )
) enable row movement;
--step4: 创建二级分区表,一级分区键二级分区键都为空; expect:合理报错
drop table if exists t_subpartition_0271;
create   table if not exists t_subpartition_0271
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0271
partition by range ( ) subpartition by range ( )
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition t_subpartition_0271 values less than( 10 )
  )
) enable row movement;

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0271;
drop tablespace if exists ts_subpartition_0271;