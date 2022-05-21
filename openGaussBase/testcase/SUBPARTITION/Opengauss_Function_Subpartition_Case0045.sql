-- @testpoint: list_list二级分区表修改：modify_clause/exchange/merge into/move,部分测试点合理报错

--test1: alter table modify_clause
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0045;
drop table if exists t_subpartition_0045_01;
drop tablespace if exists ts_subpartition_0045;
create tablespace ts_subpartition_0045 relative location 'subpartition_tablespace/subpartition_tablespace_0045';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0045
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0045
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
--step3: 分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0045(col_1,col_2);
--step4: 修改指定一级分区索引不可用; expect:合理报错
alter table t_subpartition_0045 modify partition p_list_2 unusable local indexes;

--test2: alter table exchange
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0045;
create table if not exists t_subpartition_0045
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0045
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
--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0045_01;
create table if not exists t_subpartition_0045_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0045;
--step7: 普通表插入数据; expect:成功
insert into t_subpartition_0045_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 把普通表的数据迁移到二级分区表; expect:合理报错
alter table t_subpartition_0045 exchange partition (p_list_1) with table t_subpartition_0045_01 without validation;
--step9: 查询数据; expect:成功,0条数据
select * from t_subpartition_0045;
--step10: 查询数据; expect:成功
select * from t_subpartition_0045_01;

--test3: alter table  merge into
--step11: 修改二级分区表，把多个一级分区合并为一个一级分区; expect:合理报错
alter table t_subpartition_0045 merge partitions p_list_1,p_list_2 into partition p_range_8;

--test4: alter table  move
--step12: 创建表空间; expect:成功
drop tablespace if exists ts_subpartition_0045_01;
create tablespace ts_subpartition_0045_01 relative location 'subpartition_tablespace/subpartition_tablespace_0045_01';
--step13: 修改二级分区表，移动一级分区到新的表空间; expect:合理报错
alter table t_subpartition_0045 move partition p_range_2 tablespace ts_subpartition_0045_01;

--step14: 删除表; expect:成功
drop table if exists t_subpartition_0045;
drop table if exists t_subpartition_0045_01;
drop tablespace if exists ts_subpartition_0045;
drop tablespace if exists ts_subpartition_0045_01;