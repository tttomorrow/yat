-- @testpoint: range_range二级分区表：执行算子/计划裁剪/rownum

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0292;
drop tablespace if exists ts_subpartition_0292;
create tablespace ts_subpartition_0292 relative location 'subpartition_tablespace/subpartition_tablespace_0292';

--test1: 执行算子--seq scan
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0292
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0292
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0292 values(0,0,0,0);
insert into t_subpartition_0292 values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0292 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0292 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查看执行计划; expect:成功,有seq scan执行算子
explain analyze select * from t_subpartition_0292;

--test2: 执行算子--index  scan
--step5: 二级分区键创建索引; expect:成功
drop index if exists i_subpartition_0292;
create index i_subpartition_0292 on t_subpartition_0292(col_2) local ;
--step6: 插入数据; expect:成功
insert into t_subpartition_0292 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step7: 查看执行计划; expect:成功,有index scan执行算子
explain analyze select * from t_subpartition_0292 where col_2 in  (select col_1 from t_subpartition_0292 subpartition(p_range_1_2) where col_1 >10);

--test3: 执行算子--bitmap index scan/bitmap heap scan
--step8: 查看执行计划; expect:成功,指定index scan
explain analyze select *  from t_subpartition_0292 where col_2 >500 and col_2 <8000 order by col_1;

--test4: 执行算子--subquery scan
--step9: 查看执行计划; expect:无subquery scan
explain analyze select * from (select * from t_subpartition_0292 subpartition(p_range_1_2));
--step10: 查看执行计划; expect:无subquery scan
explain analyze select * from   (select col_1 from t_subpartition_0292 subpartition(p_range_1_2) where col_1 >10) order by 1;

--test5: 执行算子--function scan
--step11: 创建函数; expect:成功
create or replace function partition_func() returns boolean as
    $$
    declare
    begin
         delete from t_subpartition_0292 where col_2=8;
         return 1;
    end
    $$ language plpgsql;
    /
--step12: 查看执行计划; expect:成功,指定function scan on func
explain (costs off) select * from partition_func ();

--step13: 创建表; expect:成功
drop table if exists t_subpartition_0292_01;
create table t_subpartition_0292_01 (a int, b int[]);
--step14: 查看执行计划; expect:成功,指定seq scan on 表
explain (costs off) select generate_series(1, 2) from (select col_2 from t_subpartition_0292) as res;

--test6: 执行算子--支持plan hint调优
drop index if exists index_01;
--step15: 查看执行计划; expect:成功,指定index scan
explain analyze select /*+ indexscan(t_subpartition_0292 index_01)*/ *  from t_subpartition_0292 where col_2 >500 and col_2 <8000 order by col_1;

--test7: 执行算子--prepare
--step16: 创建预备语句1; expect:成功
prepare p_subpartition_0292_01 as select * from   (select col_1 from t_subpartition_0292 subpartition(p_range_1_2) where col_1 >10 and col_2 <8000) order by 1;
--step17: 查看预备语句1的执行计划; expect:成功,filter: ((col_1 > 10) and (col_2 < 8000))
explain execute p_subpartition_0292_01;
--step18: 创建预备语句2; expect:成功
prepare p_subpartition_0292_02 as select * from t_subpartition_0292 where col_2 in  (select col_1 from t_subpartition_0292 subpartition(p_range_1_2) where col_1 >10);
--step19: 查看预备语句2的执行计划; expect:成功,filter: (col_1 > 10)
explain execute p_subpartition_0292_02;
--step20: 创建预备语句3; expect:成功
prepare p_subpartition_0292_03 as select * from t_subpartition_0292 where col_2 in  (select col_1 from t_subpartition_0292 subpartition(p_range_1_2) where col_1 >$1);
--step21: 查看预备语句3的执行计划; expect:成功,filter: (col_1 > $1)
explain execute p_subpartition_0292_03(100);

--step22: 删除预备语句; expect:成功
deallocate p_subpartition_0292_01;
deallocate p_subpartition_0292_02;
deallocate p_subpartition_0292_03;

--test8: 计划裁剪
--step23: 查询不同的分区数据; expect:成功
select col_1 from t_subpartition_0292 subpartition(p_range_1_2) where col_1 >10 and col_2 <8000;
select count(*) from t_subpartition_0292 subpartition(p_range_1_2) ;
select count(*) from t_subpartition_0292 subpartition(p_range_1_1) ;
select count(*) from t_subpartition_0292 subpartition(p_range_2_1) ;
select count(*) from t_subpartition_0292 subpartition(p_range_2_2) ;
--step24: 查询表数据; expect:成功,上面查询结果之和100116
select count(*) from t_subpartition_0292 ;


--test9: 分区表 +rownum 
--step25: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0292;
create table if not exists t_subpartition_0292
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0292
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
) enable row movement;
--step26: 插入数据; expect:成功
insert into t_subpartition_0292 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step27: 查询rownum数据; expect:成功
select rownum,* from t_subpartition_0292 where col_3 >98 limit 10;

--step28: 清理环境; expect:成功
drop table if exists t_subpartition_0292_01;
drop table if exists t_subpartition_0292 cascade;
drop tablespace if exists ts_subpartition_0292;