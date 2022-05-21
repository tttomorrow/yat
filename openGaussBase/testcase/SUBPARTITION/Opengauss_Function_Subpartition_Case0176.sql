-- @testpoint: list_hash二级分区表：rownum/视图/物化视图,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0176 cascade;
drop tablespace if exists ts_subpartition_0176;
create tablespace ts_subpartition_0176 relative location 'subpartition_tablespace/subpartition_tablespace_0176';
--test1: 分区表 + rownum
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0176
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0176
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step3: generate_series插入大量数据; expect:成功
insert into t_subpartition_0176 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step4: 查询数据：rownum; expect:成功
select rownum,* from t_subpartition_0176 where col_3 > 98 and rownum <10;
--step5: 查询数据：rownum/order by/desc/limit; expect:成功
select rownum,* from t_subpartition_0176 where col_3 > 98 order by rownum desc limit 2,18;

--test2: 视图
--step6: 创建视图：rownum; expect:成功
drop view if exists v_subpartition_0176;
create view v_subpartition_0176 as select * from t_subpartition_0176;
--step7: 查询视图数据; expect:成功
select * from v_subpartition_0176 limit 10;
--step8: count函数查询视图数据; expect:成功,100100条
select  count(*) from v_subpartition_0176;
--step9: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0176 where col_1 = 4;
--step10: 查询视图数据; expect:成功,数据减少,95095条
select  count(*) from v_subpartition_0176;
--step11: 查询表数据; expect:成功,数据减少,95095条
select  count(*) from t_subpartition_0176;
--step12: 更新表中指定条件的数据; expect:成功
update t_subpartition_0176 set col_1 = 4 where col_1 = 1;
--step13: 查询指定条件的视图数据; expect:成功,0条
select * from v_subpartition_0176 where col_1 = 1;
--step14: 更新视图中指定条件的数据; expect:合理报错
update v_subpartition_0176 set col_1 = 4 where col_1 = 8;

--test3: 物化视图
--step15: 创建物化视图; expect:成功
drop materialized view if exists vm_subpartition_0176;
create materialized view vm_subpartition_0176 as select * from t_subpartition_0176;
--step16: 查询物化视图数据; expect:成功
select  count(*) from vm_subpartition_0176;
--step17: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0176 where col_1 = 4;
--step18: 查询物化视图数据; expect:成功,数据条数没变
select  count(*) from vm_subpartition_0176;
--step19: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0176;
--step20: 查询物化视图数据; expect:成功,数据条数减少
select  count(*) from vm_subpartition_0176;

--step21: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0176 where col_1 = 11;
--step22: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0176 where col_1 = 4;
--step23: 更新表中指定条件的数据; expect:成功
update t_subpartition_0176 set col_1 = 18 where col_1 = 11;
--step24: 查询数据; expect:成功,数据条数没变
select count(*) from vm_subpartition_0176 where col_1 = 11;
--step25: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0176;
--step26: 查询数据; expect:成功,0条数据
select count(*) from vm_subpartition_0176 where col_1 = 11;
--step27: 更新物化视图中指定条件的数据; expect:合理报错
update vm_subpartition_0176 set col_1 = 4 where col_1 = 8;

--step28: 清理环境; expect:成功
drop view if exists v_subpartition_0176;
drop materialized view if exists vm_subpartition_0176;
drop table if exists t_subpartition_0176 cascade;
drop table if exists t_subpartition_0176_01 cascade;
drop table if exists t_subpartition_0176_02 cascade;
drop tablespace if exists ts_subpartition_0176;