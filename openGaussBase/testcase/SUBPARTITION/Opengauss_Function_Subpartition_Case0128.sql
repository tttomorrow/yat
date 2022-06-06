-- @testpoint: list_range二级分区表：强制转换/cluster,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0128;
drop tablespace if exists ts_subpartition_0128;
create tablespace ts_subpartition_0128 relative location 'subpartition_tablespace/subpartition_tablespace_0128';
--test1: 强制转换
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0128
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0128
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
insert into t_subpartition_0128 values(5.89,6.48,738.8,564.8);
--step4: 查询数据; expect:成功
select * from t_subpartition_0128;
--step5: 插入数据，强制转换; expect:合理报错
insert into t_subpartition_0128 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);

--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0128;
create table if not exists t_subpartition_0128_01
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0128;
--step7: 插入数据，强制转换; expect:合理报错
insert into t_subpartition_0128_01 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);
--step8: 查询数据，强制转换; expect:成功，0条数据
select * from t_subpartition_0128_01;

--test2: cluster(不支持)
--step9: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0128;
create table if not exists t_subpartition_0128
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0128
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
--step10: 插入数据; expect:成功
insert into t_subpartition_0128 values(5.89,6.48,738.8,564.8);
insert into t_subpartition_0128 values(10.89,6.48,738.8,564.8);
--step11: 分区键创建索引; expect:成功
drop index if exists index_01;
create index  index_01 on t_subpartition_0128(col_1,col_2);
--step12: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0128;
--step13: cluster根据索引聚簇排序; expect:合理报错
cluster t_subpartition_0128 using index_01;
--step14: cluster根据索引聚簇排序，显示进度信息; expect:合理报错
cluster verbose t_subpartition_0128 using index_01;

--step15: 清理环境; expect:成功
drop table if exists t_subpartition_0128;
drop table if exists t_subpartition_0128_01;
drop tablespace if exists ts_subpartition_0128;