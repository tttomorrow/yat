-- @testpoint: range_list二级分区表：计划裁剪

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0233;
drop tablespace if exists ts_subpartition_0233;
create tablespace ts_subpartition_0233 relative location 'subpartition_tablespace/subpartition_tablespace_0233';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0233
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0233
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
insert into t_subpartition_0233 values(0,0,0,0);
insert into t_subpartition_0233 values(-11,1,1,1),(-14,1,4,4),(-25,15,5,5),(-808,8,8,8),(-9,9,9,9);
insert into t_subpartition_0233 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0233 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--test1: 计划裁剪
--step4: where条件查询数据; expect:成功
select col_1 from t_subpartition_0233 subpartition(p_list_2_2) where col_1 >10 and col_2 <8000;
--step5: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0233 subpartition(p_list_1_1) ;
--step6: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0233 subpartition(p_list_1_2) ;
--step7: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0233 subpartition(p_list_2_1) ;
--step8: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0233 subpartition(p_list_2_2) ;
--step9: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0233 ;

--step10: 清理环境; expect:成功
drop table if exists t_subpartition_0233;
drop tablespace if exists ts_subpartition_0233;