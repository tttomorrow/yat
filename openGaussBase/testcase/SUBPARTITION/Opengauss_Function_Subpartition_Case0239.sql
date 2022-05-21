-- @testpoint: range_list二级分区表：生成列,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0239;
drop tablespace if exists ts_subpartition_0239;
create tablespace ts_subpartition_0239 relative location 'subpartition_tablespace/subpartition_tablespace_0239';
--step2: 创建二级分区表,二级分区列指定生成列; expect:合理报错
drop table if exists t_subpartition_0239;
create table t_subpartition_0239
(
    col_1 int ,
    col_2 int generated always as(2*col_4) stored ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0239
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
--step3: 创建二级分区表,普通列指定生成列; expect:成功
drop table if exists t_subpartition_0239;
create table t_subpartition_0239
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int generated always as(2*col_1) stored
)
tablespace ts_subpartition_0239
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
--step4: 插入数据; expect:成功
insert into t_subpartition_0239 values(1,1,1),(4,4,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0239(col_1,col_2,col_3)  values(31,1,1),(34,4,4),(45,5,5),(68,8,8),(70,9,9);
--step5: 查询数据; expect:成功
select * from t_subpartition_0239 partition(p_range_4);
--step6: 查询数据; expect:成功
select * from t_subpartition_0239 subpartition(p_list_4_1);
--step7: 查询数据; expect:成功
select * from t_subpartition_0239 partition(p_range_5);
--step8: 查询数据; expect:成功
select * from t_subpartition_0239 subpartition(p_range_5_subpartdefault1);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0239;
drop tablespace if exists ts_subpartition_0239;