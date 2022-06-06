-- @testpoint: range_hash二级分区表：rownum/视图/物化视图,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0342;
drop tablespace if exists ts_subpartition_0342;
create tablespace ts_subpartition_0342 relative location 'subpartition_tablespace/subpartition_tablespace_0342';

--test1: 分区表 +rownum 
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0342
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0342
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
insert into t_subpartition_0342 values (generate_series(-19, 100),generate_series(0, 100),generate_series(0, 99));
--step4: 查询rownum数据; expect:成功
select rownum,* from t_subpartition_0342 where col_3 >98 and rownum <10;
select rownum,* from t_subpartition_0342 where col_3 >98 order by rownum desc limit 2,18;

--test2: 视图
--step5: 创建视图：rownum; expect:成功
drop view if exists v_subpartition_0342;
create view v_subpartition_0342 as select * from t_subpartition_0342;
--step6: 查询视图数据; expect:成功
select * from v_subpartition_0342 limit 10;
--step7: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0342 where col_1 =4;
--step8: 查询视图数据; expect:成功,60095条
select  count(*) from v_subpartition_0342;
--step9: 查询表数据; expect:成功,60095条
select  count(*) from t_subpartition_0342;
--step10: 更新二级分区表指定数据; expect:成功
update t_subpartition_0342 set col_1 =4 where col_1=1;
--step11: 查询视图数据; expect:成功,无数据
select * from v_subpartition_0342 where col_1=1;
--step12: 更新视图指定数据; expect:合理报错
update v_subpartition_0342 set col_1 =4 where col_1=8;

--test3: 物化视图
--step13: 创建物化视图; expect:成功
drop materialized view if exists vm_subpartition_0342;
create materialized view vm_subpartition_0342 as select * from t_subpartition_0342;
--step14: 查询物化视图数据; expect:成功,60095条数据
select  count(*) from vm_subpartition_0342;
--step15: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0342 where col_1 =4;
--step16: 查询物化视图数据; expect:成功,数据条数未变化
select  count(*) from vm_subpartition_0342;
--step17: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0342;
--step18: 查询物化视图数据; expect:成功,数据条数减少
select  count(*) from vm_subpartition_0342;

--step19: count查询指定条件的物化视图数据; expect:成功,5005条数据
select count(*) from vm_subpartition_0342 where col_1=11;
--step20: count查询指定条件的物化视图数据; expect:成功,0条数据
select count(*) from vm_subpartition_0342 where col_1=4;
--step21: 更新表中指定条件的数据; expect:成功
update t_subpartition_0342 set col_1 =18 where col_1=11;
--step22: 查询数据; expect:成功,数据条数没变
select count(*) from vm_subpartition_0342 where col_1=11;
--step23: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0342;
--step24: 查询数据; expect:成功,0条数据
select count(*) from vm_subpartition_0342 where col_1=11;
--step25: 更新物化视图中指定条件的数据; expect:合理报错
update vm_subpartition_0342 set col_1 =4 where col_1=8;

--step26: 清理环境; expect:成功
drop view if exists v_subpartition_0342;
drop materialized view if exists vm_subpartition_0342;
drop table if exists t_subpartition_0342 cascade;
drop table if exists t_subpartition_0342_01 cascade;
drop table if exists t_subpartition_0342_02 cascade;
drop tablespace if exists ts_subpartition_0342;