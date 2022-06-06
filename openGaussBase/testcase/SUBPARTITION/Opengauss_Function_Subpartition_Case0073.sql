-- @testpoint: list_list二级分区表：索引,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0073;
drop tablespace if exists ts_subpartition_0073;
create tablespace ts_subpartition_0073 relative location 'subpartition_tablespace/subpartition_tablespace_0073';
--test1: 索引
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0073
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0073
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
    subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
    subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step3: 一级分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0073;
create unique index  i_subpartition_0073 on t_subpartition_0073(col_1);
--step4: 二级分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0073;
create unique index  i_subpartition_0073 on t_subpartition_0073(col_2);
--step5: 2个分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0073;
create unique index  i_subpartition_0073 on t_subpartition_0073(col_1,col_2);
--step6: 同一列存在local索引,创建global索引; expect:合理报错
create unique index i_subpartition_0073 on t_subpartition_0073(col_1,col_2) global;
--step7: 分区键创建local唯一索引; expect:合理报错
drop index if exists i_subpartition_0073;
create  unique index i_subpartition_0073 on t_subpartition_0073(col_1) local;
--step8: 分区键创建global唯一索引; expect:成功
drop index if exists i_subpartition_0073_01;
create unique index i_subpartition_0073_01 on t_subpartition_0073(col_1) global;
--step9: 删除索引; expect:成功
drop index if exists i_subpartition_0073;
drop index if exists i_subpartition_0073_01;

--step10: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0073;
drop tablespace if exists ts_subpartition_0073;