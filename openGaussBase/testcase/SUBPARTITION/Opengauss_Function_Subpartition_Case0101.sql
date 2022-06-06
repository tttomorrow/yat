-- @testpoint: list_range二级分区表修改：drop分区键和非分区键/drop分区,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0101;
drop tablespace if exists ts_subpartition_0101;
create tablespace ts_subpartition_0101 relative location 'subpartition_tablespace/subpartition_tablespace_0101';

--test1: alter table drop --字段(分区键和非分区键)
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0101
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0101
partition by list (col_1) subpartition by range (col_2)
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0101 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step4: 查询全部数据; expect:成功
select * from t_subpartition_0101;
--step5: 修改二级分区表,删除非分区键; expect:成功
alter table t_subpartition_0101 drop column col_4;
--step6: 修改二级分区表,删除一级分区键; expect:合理报错
alter table t_subpartition_0101 drop column col_1;
--step7: 修改二级分区表,删除二级分区键; expect:合理报错
alter table t_subpartition_0101 drop column col_2;

--test2: alter table drop --分区
--step8: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0101;
create table if not exists t_subpartition_0101
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0101
partition by list (col_1) subpartition by range (col_2)
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
--step9: 插入数据; expect:成功
insert into t_subpartition_0101 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step10: 修改二级分区表,删除一级分区; expect:成功
alter table t_subpartition_0101 drop partition p_list_2;
--step11: 修改二级分区表,删除二级分区; expect:成功
alter table t_subpartition_0101 drop subpartition p_range_4_1;

--step12: 清理环境; expect:成功
drop table if exists t_subpartition_0101;
drop tablespace if exists ts_subpartition_0101;