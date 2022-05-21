-- @testpoint: list_range二级分区表：计划裁剪

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0118;
drop tablespace if exists ts_subpartition_0118;
create tablespace ts_subpartition_0118 relative location 'subpartition_tablespace/subpartition_tablespace_0118';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0118
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0118
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
insert into t_subpartition_0118 values(0,0,0,0);
insert into t_subpartition_0118 values(-11,1,1,1),(-14,1,4,4),(-25,15,5,5),(-808,8,8,8),(-9,9,9,9);
insert into t_subpartition_0118 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0118 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--test1: 执行算子--prepare
--step4: 创建预备语句1; expect:成功
prepare p_subpartition_0118_01 as select * from (select col_1 from t_subpartition_0118 subpartition(p_list_2_subpartdefault1) where col_1 >10 and col_2 <8000) order by 1;
--step5: 查看预备语句1的执行计划; expect:成功,filter: ((col_1 > 10) and (col_2 < 8000))
explain execute p_subpartition_0118_01;
--step6: 创建预备语句2; expect:成功
prepare p_subpartition_0118_02 as select * from t_subpartition_0118 where col_2 in  (select col_1 from t_subpartition_0118 subpartition(p_list_2_subpartdefault1) where col_1 >10);
--step7: 查看预备语句2的执行计划; expect:成功,filter: (col_1 > 10)
explain execute p_subpartition_0118_02;
--step8: 创建预备语句3; expect:成功
prepare p_subpartition_0118_03 as select * from t_subpartition_0118 where col_2 in  (select col_1 from t_subpartition_0118 subpartition(p_list_2_subpartdefault1) where col_1 >$1);
--step9: 查看预备语句3的执行计划; expect:成功,filter: (col_1 > $1)
explain execute p_subpartition_0118_03(100);

--step10: 删除预备语句; expect:成功
deallocate p_subpartition_0118_01;
deallocate p_subpartition_0118_02;
deallocate p_subpartition_0118_03;

--test2: 计划裁剪
--step11: 清空表数据; expect:成功
truncate t_subpartition_0118;
--step12: generate_series插入大量数据; expect:成功
insert into t_subpartition_0118 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step13: 查看分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0118') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0118')) b where a.parentid = b.oid order by a.relname;

--step14: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_1_1) ;
--step15: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_1_2) ;
--step16: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_1_3) ;
--step17: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_1_4) ;
--step18: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_1_5) ;
--step19: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_list_2_subpartdefault1) ;
--step20: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_3_1) ;
--step21: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_3_2) ;
--step22: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_4_1) ;
--step23: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_4_2) ;
--step24: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_4_3) ;
--step25: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_4_4) ;
--step26: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_4_5) ;
--step27: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_5_1) ;
--step28: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_6_1) ;
--step29: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_6_2) ;
--step30: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_6_3) ;
--step31: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_6_4) ;
--step32: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_range_6_5) ;
--step33: 查询指定二级分区数据; expect:成功
select count(*) from t_subpartition_0118 subpartition(p_list_7_subpartdefault1) ;
--step34: 查询数据; expect:成功,数据数量为上面二级分区数据数量之和100100
select count(*) from t_subpartition_0118;

--step35: 清理环境; expect:成功
drop table if exists t_subpartition_0118;
drop tablespace if exists ts_subpartition_0118;