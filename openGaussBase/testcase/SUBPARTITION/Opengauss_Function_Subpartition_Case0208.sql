-- @testpoint: range_list二级分区表：分区键为表达式/分区数0,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0208;
drop tablespace if exists ts_subpartition_0208;
create tablespace ts_subpartition_0208 relative location 'subpartition_tablespace/subpartition_tablespace_0208';

--test1: 分区键 --分区键为表达式--不支持
--step2: 创建二级分区表,一级分区键为表达式; expect:合理报错
create   table if not exists t_subpartition_0207
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0207
partition by range (col_1 +1) subpartition by list ( col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition t_subpartition_0207   values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--test2: 分区数--0个
--step3: 创建二级分区表,一级分区与二级分区数都为0; expect:合理报错
drop table if exists t_subpartition_0208;
create   table if not exists t_subpartition_0208
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0208
partition by range (col_1) subpartition by list (col_2)()
 enable row movement;

--step4: 创建二级分区表，二级分区数都为0; expect:成功
drop table if exists t_subpartition_0208;
create   table if not exists t_subpartition_0208
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0208
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30 )
) enable row movement;

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0208;
drop tablespace if exists ts_subpartition_0208;