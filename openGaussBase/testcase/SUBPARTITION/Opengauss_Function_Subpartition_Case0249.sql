-- @testpoint: range_list二级分区表：cluster/强制转换,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0249;
drop tablespace if exists ts_subpartition_0249;
create tablespace ts_subpartition_0249 relative location 'subpartition_tablespace/subpartition_tablespace_0249';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0249
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0249
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0249 values(5.89,6.48,738.8,564.8);
insert into t_subpartition_0249 values(10.89,6.48,738.8,564.8);
--step4: 创建索引; expect:成功
create index  index_01 on t_subpartition_0249(col_1,col_2);
--step5: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0249;
--step6: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0249 using index_01;
--step7: cluster聚簇排序; expect:合理报错
cluster verbose t_subpartition_0249 using index_01;

--step8: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0249;
create table if not exists t_subpartition_0249
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0249
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
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
--step9: 插入数据; expect:成功
insert into t_subpartition_0249 values(5.89,6.48,738.8,564.8);
--step10: 查询数据; expect:成功,小数转换为整数
select * from t_subpartition_0249;
--step11: 插入超出范围数据; expect:合理报错
insert into t_subpartition_0249 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);

--step12: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0249;
create table if not exists t_subpartition_0249
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0249;
--step13: 插入超出范围数据; expect:合理报错
insert into t_subpartition_0249 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);
--step14: 查询数据; expect:成功,无数据
select * from t_subpartition_0249;

--step15: 清理环境; expect:成功
drop table if exists t_subpartition_0249;
drop tablespace if exists ts_subpartition_0249;
