-- @testpoint: list_list二级分区表：local/global/unlogged,测试点合理报错

--step1: 创建二级分区表,指定local; expect:合理报错
drop table if exists t_subpartition_0039;
create local temp table t_subpartition_0039
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
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
--step2: 创建二级分区表,指定global; expect:合理报错
drop table if exists t_subpartition_0039;
create global temp table t_subpartition_0039
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
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
--step3: 创建二级分区表,指定unlogged; expect:合理报错
drop table if exists t_subpartition_0039;
create unlogged table t_subpartition_0039
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
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

--step4: 删除表; expect:成功
drop table if exists t_subpartition_0039;