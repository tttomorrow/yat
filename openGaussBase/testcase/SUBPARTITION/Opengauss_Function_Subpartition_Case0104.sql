-- @testpoint: list_range二级分区表：insert on duplicate key update,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0104;
drop tablespace if exists ts_subpartition_0104;
create tablespace ts_subpartition_0104 relative location 'subpartition_tablespace/subpartition_tablespace_0104';

--test1: insert --insert  on duplicate key update -唯一索引
create table if not exists t_subpartition_0104
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0104
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
--step2: 分区键创建唯一local索引; expect:成功
create unique index on t_subpartition_0104(col_1,col_2) local;
--step3: 插入数据; expect:成功
insert into t_subpartition_0104 values(1,11,1,1);
--step4: 插入数据,指定on duplicate key update nothing; expect:成功
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update nothing;
--step5: 查询数据; expect:成功,1条数据
select * from t_subpartition_0104 subpartition (p_list_2_subpartdefault1);
--step6: 插入重复数据; expect:合理报错
insert into t_subpartition_0104 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step7: 插入不重复数据; expect:成功
insert into t_subpartition_0104 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 查询指定二级分区数据; expect:成功,5条数据
select * from t_subpartition_0104 subpartition (p_list_2_subpartdefault1);
--step9: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update col_1=10;
--step10: 插入重复数据更新二级分区键; expect:合理报错
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update col_2=10;
--step11: 插入重复数据更新普通列; expect:成功
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update col_3=10;
--step12: 查询指定二级分区数据; expect:成功,5条数据
select * from t_subpartition_0104 subpartition (p_list_2_subpartdefault1);

--test2: insert --insert  on duplicate key update -local索引
--step13: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0104;
create table if not exists t_subpartition_0104
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0104
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
--step14: 分区键创建local索引; expect:成功
create index on t_subpartition_0104(col_1) local;
--step15: 插入数据; expect:成功
insert into t_subpartition_0104 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step16: 查询数据; expect:成功,5条数据
select * from t_subpartition_0104 subpartition (p_list_2_subpartdefault1);
--step17: 插入重复数据更新一级分区键; expect:成功
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update col_1=10;
--step18: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update col_2=10;
--step19: 插入重复数据更新一级分区键换二级分区; expect:成功
insert into t_subpartition_0104 values(1,11,1,1) on duplicate key update col_2=1;
--step20: 查询数据; expect:成功,0条数据
select * from t_subpartition_0104 subpartition (p_list_2_subpartdefault1) where col_2<5;

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0104;
drop tablespace if exists ts_subpartition_0104;