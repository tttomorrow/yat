-- @testpoint: list_range二级分区表：delete

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0108;
drop tablespace if exists ts_subpartition_0108;
create tablespace ts_subpartition_0108 relative location 'subpartition_tablespace/subpartition_tablespace_0108';
--test1: delete table
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0108
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0108
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
insert into t_subpartition_0108 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0108 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0108 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0108 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0108 values(-8,18,1);
--step4: 查询数据; expect:成功
select * from t_subpartition_0108;
--step5: 查询指定二级分区数据; expect:成功，4条数据
select * from t_subpartition_0108 subpartition(p_list_2_subpartdefault1);
--step6: 查询指定二级分区数据; expect:成功，4条数据
select * from t_subpartition_0108 subpartition(p_range_3_2);
--step7: 删除表数据; expect:成功
delete from  t_subpartition_0108;
--step8: 查询表数据; expect:成功，0条数据
select * from t_subpartition_0108;
--step9: 查询指定二级分区数据; expect:成功，0条数据
select * from t_subpartition_0108 subpartition(p_list_2_subpartdefault1);
--step10: 查询指定二级分区数据; expect:成功，0条数据
select * from t_subpartition_0108 subpartition(p_range_3_2);

--test2: delete  where
--step11: 插入数据; expect:成功
insert into t_subpartition_0108 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0108 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0108 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0108 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0108 values(-8,18,1);
--step12: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0108 where col_1 >18 ;
--step13: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0108 where col_2 <10 and col_3>5;
--step14: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0108 where col_2 <50 and col_3>5;
--step15: 查询数据; expect:成功，10条数据
select * from t_subpartition_0108;
 --step16: 查询指定二级分区数据; expect:成功，1条数据
select * from t_subpartition_0108 subpartition(p_range_1_1);
 --step17: 查询指定二级分区数据; expect:成功，0条数据
select * from t_subpartition_0108 subpartition(p_range_1_2);
 --step18: 查询指定二级分区数据; expect:成功，1条数据
select * from t_subpartition_0108 subpartition(p_range_1_3);
 --step19: 查询指定二级分区数据; expect:成功，1条数据
select * from t_subpartition_0108 subpartition(p_range_1_4);
 --step20: 查询指定二级分区数据; expect:成功，0条数据
select * from t_subpartition_0108 subpartition(p_range_1_5);
 --step21: 查询指定二级分区数据; expect:成功，2条数据
select * from t_subpartition_0108 subpartition(p_list_2_subpartdefault1);
 --step22: 查询指定二级分区数据; expect:成功，1条数据
select * from t_subpartition_0108 subpartition(p_range_3_1);
 --step23: 查询指定二级分区数据; expect:成功，4条数据
select * from t_subpartition_0108 subpartition(p_range_3_2);
--step24: 删除指定条件的数据; expect:成功
delete  t_subpartition_0108 where col_2-100>10;
--step25: 删除指定条件的数据; expect:成功
delete  t_subpartition_0108 where col_2-100>10;
--step26: 删除指定条件的数据; expect:成功
delete  t_subpartition_0108 where col_2/5>1;
--step27: 查询数据; expect:成功，4条数据
select * from t_subpartition_0108;
--step28: 查询数据; expect:成功，2条数据
select * from t_subpartition_0108 subpartition(p_list_2_subpartdefault1);
--step29: 查询数据; expect:成功，1条数据
select * from t_subpartition_0108 subpartition(p_range_1_3);
--step30: 查询数据; expect:成功，1条数据
select * from t_subpartition_0108 subpartition(p_range_1_1);
--step31: 查询数据; expect:成功，0条数据
select * from t_subpartition_0108 subpartition(p_range_1_2);

--step32: 清理环境; expect:成功
drop table if exists t_subpartition_0108;
drop tablespace if exists ts_subpartition_0108;