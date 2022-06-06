-- @testpoint: list_range二级分区表：序列--分区列序列

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0114;
drop tablespace if exists ts_subpartition_0114;
create tablespace ts_subpartition_0114 relative location 'subpartition_tablespace/subpartition_tablespace_0114';

--test1: 序列--分区列序列
--step2: 创建二级分区表，声明分区键的类型为序列整型; expect:成功
create table if not exists t_subpartition_0114
(
    col_1 serial ,
    col_2 serial,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0114
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
insert into t_subpartition_0114(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step4: 查询指定二级分区数据; expect:成功，有数据
select * from t_subpartition_0114 subpartition(p_list_2_subpartdefault1);
--step5: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0114 truncate subpartition p_list_2_subpartdefault1;
--step6: 查询指定二级分区数据; expect:成功，无数据
select * from t_subpartition_0114 subpartition(p_list_2_subpartdefault1);
--step7: 插入数据; expect:成功
insert into t_subpartition_0114(col_2,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0114(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step8: 查询指定二级分区数据; expect:成功，有数据
select * from t_subpartition_0114 subpartition(p_list_2_subpartdefault1);
--step9: 插入数据; expect:成功
insert into t_subpartition_0114(col_2,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0114(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0114(col_2,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0114(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step10: 查询指定二级分区数据; expect:成功，有数据
select * from t_subpartition_0114 subpartition(p_range_3_1);

--step11: 清理环境; expect:成功
drop table if exists t_subpartition_0114;
drop tablespace if exists ts_subpartition_0114;