-- @testpoint: list_list二级分区表修改：rename约束/字段/分区/表,部分测试点合理报错

--test1: alter table rename --约束
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0044;
drop tablespace if exists ts_subpartition_0044;
create tablespace ts_subpartition_0044 relative location 'subpartition_tablespace/subpartition_tablespace_0044';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0044
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0044
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
--step3: 修改二级分区表，重命名约束; expect:成功
alter table t_subpartition_0044 rename  constraint t_subpartition_0044_col_4_check to drop_check;
--step4: 插入违反约束的数据; expect:合理报错
insert into t_subpartition_0044 values(1,1,1,null);

--test2: alter table rename --字段
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0044;
create table if not exists t_subpartition_0044
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
    check (col_4 is not null)
)tablespace ts_subpartition_0044
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
--step6: 修改二级分区表，重命名非分区键; expect:成功
alter table t_subpartition_0044 rename column col_4 to col_4444;
--step7: 修改二级分区表，重命名分区键; expect:成功
alter table t_subpartition_0044 rename column col_2 to col_22222;

--test3: alter table rename --分区
--step8: 二级分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0044(col_22222);
--step9: 修改二级分区表，重命名一级分区; expect:合理报错
alter table t_subpartition_0044 rename partition p_range_2 to p_range_2_2222222;
--step10: 查看分区数据; expect:成功，分区名未修改
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0044') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0044')) b where a.parentid = b.oid order by a.relname;

--test4: alter table rename --表
--step11: 修改二级分区表，重命名二级分区表; expect:合理报错
alter table t_subpartition_0044 rename to hahahahahah;

--step12: 删除表; expect:成功
drop table if exists t_subpartition_0044;
drop tablespace if exists ts_subpartition_0044;