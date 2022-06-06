-- @testpoint: list_range二级分区表：分区键为表达式/分区数0,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0094;
drop tablespace if exists ts_subpartition_0094;
create tablespace ts_subpartition_0094 relative location 'subpartition_tablespace/subpartition_tablespace_0094';

--test2: 分区键 --分区键为表达式--不支持
--step2: 创建二级分区表,一级分区键为表达式; expect:合理报错
drop table if exists t_subpartition_0094;
create   table if not exists t_subpartition_0094
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0094
partition by list (upper(col_1)) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;

--test3: 分区数--0个
--step3: 创建二级分区表,一级分区与二级分区数都为0; expect:合理报错
create   table if not exists t_subpartition_0094
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0094
partition by list (col_1) subpartition by range (col_2)
(
) enable row movement;
--step4: 创建二级分区表,二级分区数为0; expect:成功
drop table if exists t_subpartition_0094;
create   table if not exists t_subpartition_0094
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0094
partition by list (col_1) subpartition by range (col_2)
(
   partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 ),
   partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
   partition p_list_3 values(11,12,13,14,15,16,17,18,19,20),
   partition p_list_4 values(21,22,23,24,25,26,27,28,29,30),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50),
   partition p_list_7 values(default)
) enable row movement;
--step5: 查看分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0094') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0094')) b where a.parentid = b.oid order by a.relname;

--step6: 清理环境; expect:成功
drop table if exists t_subpartition_0094;
drop tablespace if exists ts_subpartition_0094;