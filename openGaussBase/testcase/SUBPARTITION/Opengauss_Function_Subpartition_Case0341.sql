-- @testpoint: range_hash二级分区表：执行算子/计划裁剪

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0341;
drop tablespace if exists ts_subpartition_0341;
create tablespace ts_subpartition_0341 relative location 'subpartition_tablespace/subpartition_tablespace_0341';

--test1: 执行算子--seq scan
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0341
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0341
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0341 values(0,0,0,0);
insert into t_subpartition_0341 values(-11,1,1,1),(-14,1,4,4),(-25,15,5,5),(-808,8,8,8),(-9,9,9,9);
insert into t_subpartition_0341 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0341 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查看执行计划; expect:成功,有seq scan执行算子
explain analyze select * from t_subpartition_0341;


--test2: 执行算子--index  scan
--step5: 二级分区键创建索引; expect:成功
drop index if exists i_subpartition_0341;
create index index_01 on t_subpartition_0341(col_2) local ;
--step6: 插入数据; expect:成功
insert into t_subpartition_0341 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step7: 查看执行计划; expect:成功,有index scan执行算子
explain analyze select * from t_subpartition_0341 where col_2 in  (select col_1 from t_subpartition_0341 subpartition(p_range_2_subpartdefault1) where col_1 >10);

--test3: 执行算子--bitmap index scan/bitmap heap scan
--step8: 查看执行计划; expect:成功,有bitmap index scan/bitmap heap scan
explain analyze select *  from t_subpartition_0341 where col_2 >500 and col_2 <8000 order by col_1;

--test4: 执行算子--支持plan hint调优
drop index if exists index_01;
create index index_01 on t_subpartition_0341(col_2);
--step9: 查看执行计划; expect:成功,指定index scan

--test5: 执行算子--prepare
--step10: 创建预备语句1; expect:成功
prepare p_subpartition_0341_01 as select * from   (select col_1 from t_subpartition_0341 subpartition(p_range_2_subpartdefault1) where col_1 >10 and col_2 <8000) order by 1;
--step11: 查看预备语句1的执行计划; expect:成功,filter: ((col_1 > 10) and (col_2 < 8000))
explain execute p_subpartition_0341_01;
--step12: 创建预备语句2; expect:成功
prepare p_subpartition_0341_02 as select * from t_subpartition_0341 where col_2 in  (select col_1 from t_subpartition_0341 subpartition(p_range_2_subpartdefault1) where col_1 >10);
--step13: 查看预备语句2的执行计划; expect:成功,filter: (col_1 > 10)
explain execute p_subpartition_0341_02;
--step14: 创建预备语句3; expect:成功
prepare p_subpartition_0341_03 as select * from t_subpartition_0341 where col_2 in  (select col_1 from t_subpartition_0341 subpartition(p_range_2_subpartdefault1) where col_1 >$1);
--step15: 查看预备语句3的执行计划; expect:成功,filter: (col_1 > $1)
explain execute p_subpartition_0341_03(100);

--step16: 删除预备语句; expect:成功
deallocate p_subpartition_0341_01;
deallocate p_subpartition_0341_02;
deallocate p_subpartition_0341_03;

--test6: 计划裁剪
--step17: 插入数据; expect:成功
insert into t_subpartition_0341 values (generate_series(-19, 100),generate_series(0, 100),generate_series(0, 99));
--step18: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0341') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0341')) b where a.parentid = b.oid order by a.relname;

--step19: 查询不同的分区数据; expect:成功
select count(*) from t_subpartition_0341 subpartition(p_hash_1_1) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_1_2) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_1_3) ;
select count(*) from t_subpartition_0341 subpartition(p_range_2_subpartdefault1) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_3_1) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_3_2) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_3_3) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_4_1) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_4_2) ;
select count(*) from t_subpartition_0341 subpartition(p_hash_4_3) ;
select count(*) from t_subpartition_0341 subpartition(p_range_5_subpartdefault1) ;
--step20: 查询表数据; expect:成功,各分区查询结果之和160716
select count(*) from t_subpartition_0341;

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0341;
drop tablespace if exists ts_subpartition_0341;