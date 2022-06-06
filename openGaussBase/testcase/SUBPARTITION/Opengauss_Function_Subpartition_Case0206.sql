-- @testpoint: range_list二级分区表：分区键1个存在/不存在,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0206;
drop tablespace if exists ts_subpartition_0206;
create tablespace ts_subpartition_0206 relative location 'subpartition_tablespace/subpartition_tablespace_0206';

--test1: 分区键 --1个
--step2: 创建二级分区表,二级分区键1个且列存在; expect:成功
create   table if not exists t_subpartition_0206
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0206
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition t_subpartition_0206   values ( default )
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
--step3: 创建二级分区表,二级分区键1个且列不存在; expect:合理报错
drop table if exists t_subpartition_0206;
create   table if not exists t_subpartition_0206
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0206
partition by range (col_1) subpartition by list (col_5)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition t_subpartition_0206   values ( default )
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
--step4: 创建二级分区表,一级分区键1个且列不存在; expect:合理报错
drop table if exists t_subpartition_0206;
create   table if not exists t_subpartition_0206
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0206
partition by range (col_5) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
    subpartition t_subpartition_0206   values ( default )
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

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0206;
drop tablespace if exists ts_subpartition_0206;
