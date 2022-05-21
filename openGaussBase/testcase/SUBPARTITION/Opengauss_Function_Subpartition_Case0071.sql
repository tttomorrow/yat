-- @testpoint: list_list二级分区表：强制转换/cluster,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0071;
drop tablespace if exists ts_subpartition_0071;
create tablespace ts_subpartition_0071 relative location 'subpartition_tablespace/subpartition_tablespace_0071';
--test1: 强制转换
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0071
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0071
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0071 values(5.89,6.48,738.8,564.8);
--step4: 查询数据; expect:成功
select * from t_subpartition_0071;
--step5: 插入数据，强制转换; expect:合理报错
insert into t_subpartition_0071 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);

--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0071;
create table if not exists t_subpartition_0071_01
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0071;
--step7: 插入数据，强制转换; expect:合理报错
insert into t_subpartition_0071_01 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);
--step8: 查询数据，强制转换; expect:成功，0条数据
select * from t_subpartition_0071_01;

--test2: cluster(不支持)
--step9: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0071;
create table if not exists t_subpartition_0071
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0071
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
--step10: 插入数据; expect:成功
insert into t_subpartition_0071 values(5.89,6.48,738.8,564.8);
insert into t_subpartition_0071 values(10.89,6.48,738.8,564.8);
--step11: 分区键创建索引; expect:成功
drop index if exists index_01;
create index  index_01 on t_subpartition_0071(col_1,col_2);
--step12: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0071;
--step13: cluster根据索引聚簇排序; expect:合理报错
cluster t_subpartition_0071 using index_01;
--step14: cluster根据索引聚簇排序，显示进度信息; expect:合理报错
cluster verbose t_subpartition_0071 using index_01;

--step15: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0071;
drop table if exists t_subpartition_0071_01;
drop tablespace if exists ts_subpartition_0071;