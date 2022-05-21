-- @testpoint: list_list二级分区表：计划裁剪

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0061;
drop tablespace if exists ts_subpartition_0061;
create tablespace ts_subpartition_0061 relative location 'subpartition_tablespace/subpartition_tablespace_0061';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0061
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0061
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
insert into t_subpartition_0061 values(0,0,0,0);
insert into t_subpartition_0061 values(-11,1,1,1),(-14,1,4,4),(-25,15,5,5),(-808,8,8,8),(-9,9,9,9);
insert into t_subpartition_0061 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0061 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--test1: 执行算子--prepare
--step3: 创建预备语句1; expect:成功
prepare p_subpartition_0061_01 as select * from (select col_1 from t_subpartition_0061 subpartition(p_list_2_2) where col_1 >10 and col_2 <8000) order by 1;
--step4: 查看预备语句1的执行计划; expect:成功，filter: ((col_1 > 10) and (col_2 < 8000))
explain execute p_subpartition_0061_01;
--step5: 创建预备语句2; expect:成功
prepare p_subpartition_0061_02 as select * from t_subpartition_0061 where col_2 in  (select col_1 from t_subpartition_0061 subpartition(p_list_2_2) where col_1 >10);
--step6: 查看预备语句2的执行计划; expect:成功，filter: (col_1 > 10)
explain execute p_subpartition_0061_02;
--step7: 创建预备语句3; expect:成功
prepare p_subpartition_0061_03 as select * from t_subpartition_0061 where col_2 in (select col_1 from t_subpartition_0061 subpartition(p_list_2_2) where col_1 >$1);
--step8: 查看预备语句3的执行计划; expect:成功，filter: (col_1 > $1)
explain execute p_subpartition_0061_03(100);

--step9: 删除预备语句; expect:成功
deallocate p_subpartition_0061_01;
deallocate p_subpartition_0061_02;
deallocate p_subpartition_0061_03;

--test2: 计划裁剪
--step10: 清空表数据; expect:成功
truncate t_subpartition_0061;
--step11: generate_series插入大量数据; expect:成功
insert into t_subpartition_0061 values (generate_series(-19, 49),generate_series(-10, 100),generate_series(0, 99));
--step12: 查看分区信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0061') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0061')) b where a.parentid = b.oid order by a.relname;

--step13: 查询指定二级分区数据; expect:成功，3300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_1_1 ) ;
--step14: 查询指定二级分区数据; expect:成功，33700条数据
select count(*) from t_subpartition_0061 subpartition(p_list_1_2 ) ;
--step15: 查询指定二级分区数据; expect:成功，3400条数据
select count(*) from t_subpartition_0061 subpartition(p_list_2_1 ) ;
--step16: 查询指定二级分区数据; expect:成功，23600条数据
select count(*) from t_subpartition_0061 subpartition(p_list_2_2) ;
--step17: 查询指定二级分区数据; expect:成功，3300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_2_3 ) ;
--step18: 查询指定二级分区数据; expect:成功，3300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_2_4 ) ;
--step19: 查询指定二级分区数据; expect:成功，3400条数据
select count(*) from t_subpartition_0061 subpartition(p_list_2_5) ;
--step20: 查询指定二级分区数据; expect:成功，37000条数据
select count(*) from t_subpartition_0061 subpartition(p_list_3_2) ;
--step21: 查询指定二级分区数据; expect:成功，33300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_4_subpartdefault1) ;
--step22: 查询指定二级分区数据; expect:成功，3300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_5_1 ) ;
--step23: 查询指定二级分区数据; expect:成功，23700条数据
select count(*) from t_subpartition_0061 subpartition(p_list_5_2) ;
--step24: 查询指定二级分区数据; expect:成功，3300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_5_3 ) ;
--step25: 查询指定二级分区数据; expect:成功，3400条数据
select count(*) from t_subpartition_0061 subpartition(p_list_5_4) ;
--step26: 查询指定二级分区数据; expect:成功，3300条数据
select count(*) from t_subpartition_0061 subpartition(p_list_5_5 ) ;
--step27: 查询指定二级分区数据; expect:成功，37000条数据
select count(*) from t_subpartition_0061 subpartition(p_list_6_subpartdefault1) ;
--step28: 查询指定二级分区数据; expect:成功，37000条数据
select count(*) from t_subpartition_0061 subpartition(p_list_7_1) ;
--step29: 查询数据; expect:成功，数据数量为上面二级分区数据数量之和255300
select count(*) from t_subpartition_0061;

--step30: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0061;
drop tablespace if exists ts_subpartition_0061;