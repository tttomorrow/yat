-- @testpoint: range_list二级分区表：insert on duplicate key update,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0219;
drop tablespace if exists ts_subpartition_0219;
create tablespace ts_subpartition_0219 relative location 'subpartition_tablespace/subpartition_tablespace_0219';
drop tablespace if exists ts_subpartition_0219_01;
create tablespace ts_subpartition_0219_01 relative location 'subpartition_tablespace/subpartition_tablespace_0219_01';

--test1: insert --insert  on duplicate key update -唯一索引
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0219
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0219
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
--step3: 分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0219(col_1,col_2);
--step4: 插入数据,指定on duplicate key update nothing; expect:成功
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update nothing;
--step5: 查询数据; expect:成功,有数据
select * from t_subpartition_0219 subpartition (p_list_2_2);
--step6: 插入不重复数据; expect:成功
insert into t_subpartition_0219 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step7: 插入重复数据; expect:合理报错
insert into t_subpartition_0219 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 查询指定二级分区数据; expect:成功,5条数据
select * from t_subpartition_0219 subpartition (p_list_2_2);
--step9: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update col_1=10;
--step10: 插入重复数据更新二级分区键; expect:合理报错
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update col_2=10;
--step11: 插入重复数据更新普通列; expect:成功
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update col_3=10;
--step12: 查询指定二级分区数据; expect:成功,数据更新
select * from t_subpartition_0219 subpartition (p_list_2_2);

--test2: insert --insert  on duplicate key update -local索引
--step13: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0219;
create table if not exists t_subpartition_0219
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0219
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
--step14: 分区键创建local索引; expect:成功
create index on t_subpartition_0219(col_1) local;
--step15: 插入数据; expect:成功
insert into t_subpartition_0219 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step16: 查询数据; expect:成功
select * from t_subpartition_0219 subpartition (p_list_2_2);
--step17: 插入重复数据更新一级分区键; expect:成功
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update col_1=10;
--step18: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update col_2=10;
--step19: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0219 values(1,11,1,1) on duplicate key update col_2=1;
--step20: 查询数据; expect:成功,无数据
select * from t_subpartition_0219 subpartition (p_list_2_2) where col_2<5;
--step21: 分区键创建local索引,并指定索引分区的名称; expect:成功
drop index  if exists i_subpartition_0219;
create index i_subpartition_0219 on t_subpartition_0219(col_2) local(
partition index_p_range_1(subpartition index_p_list_1_1,subpartition index_p_list_1_2),
partition index_p_range_2(subpartition index_p_list_2_1,subpartition index_p_list_2_2),
partition index_p_range_3(subpartition index_p_list_3_1),
partition index_p_range_4(subpartition index_p_list_4_1),
partition index_p_range_5(subpartition index_p_list_5_1)
);

--step22: 清理环境; expect:成功
drop table if exists t_subpartition_0219;
drop tablespace if exists ts_subpartition_0219;