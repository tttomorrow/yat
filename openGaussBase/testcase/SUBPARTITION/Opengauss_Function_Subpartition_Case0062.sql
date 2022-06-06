-- @testpoint: list_list二级分区表：rownum/视图/物化视图,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0062;
drop tablespace if exists ts_subpartition_0062;
create tablespace ts_subpartition_0062 relative location 'subpartition_tablespace/subpartition_tablespace_0062';
--test1: 分区表 + rownum
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0062
(
    col_1 int ,
    col_2 int,
	col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0062
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
--step3: generate_series插入大量数据; expect:成功
insert into t_subpartition_0062 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step4: 查询指定条件数据; expect:成功
select rownum,* from t_subpartition_0062 where col_3 >98 and rownum <10;
select rownum,* from t_subpartition_0062 where col_3 >98 order by rownum desc limit 2,18;
--step5：with as查询语句; expect:成功
with t as materialized (select * from t_subpartition_0062 where col_1<100) select * from t where t.col_1 >10 limit 10;
with t as not materialized(select * from t_subpartition_0062 where col_1<100) select * from t where t.col_1 >10 limit 10;

--test2: 视图
--step6: 创建视图：rownum; expect:成功
drop view if exists v_subpartition_0062;
create view v_subpartition_0062 as select * from t_subpartition_0062;
--step7: 查询视图数据; expect:成功
select * from v_subpartition_0062 limit 10;
--step8: count函数查询视图数据; expect:成功，100100条
select  count(*) from v_subpartition_0062;
--step9: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0062 where col_1 =4;
--step10: 查询视图数据; expect:成功，数据减少，95095条
select  count(*) from v_subpartition_0062;
--step11: 更新表中指定条件的数据; expect:成功
update t_subpartition_0062 set col_1 =4 where col_1=1;
--step12: 查询指定条件的视图数据; expect:成功，0条
select * from v_subpartition_0062 where col_1=1;
--step13: 更新视图中指定条件的数据; expect:合理报错
update v_subpartition_0062 set col_1 =4 where col_1=8;

--test3: 物化视图
--step14: 创建物化视图; expect:成功
drop materialized view if exists vm_subpartition_0062;
create materialized view vm_subpartition_0062 as select * from t_subpartition_0062;
--step15: 查询物化视图数据; expect:成功
select  count(*) from vm_subpartition_0062;
--step16: 删除表中指定条件的数据数据; expect:成功
delete t_subpartition_0062 where col_1 =4;
--step17: 查询物化视图数据; expect:成功，数据条数没变
select  count(*) from vm_subpartition_0062;
--step18: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0062;
--step19: 查询物化视图数据; expect:成功，数据条数减少
select  count(*) from vm_subpartition_0062;

--step20: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0062 where col_1=11;
--step21: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0062 where col_1=4;
--step22: 更新表中指定条件的数据; expect:成功
update t_subpartition_0062 set col_1 =18 where col_1=11;
--step23: 查询数据; expect:成功，数据条数没变
select count(*) from vm_subpartition_0062 where col_1=11;
--step24: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0062;
--step25: 查询数据; expect:成功，0条数据
select count(*) from vm_subpartition_0062 where col_1=11;
--step26: 更新物化视图中指定条件的数据; expect:合理报错
update vm_subpartition_0062 set col_1 =4 where col_1=8;

--test4: 普通表
--step27: 创建普通表; expect:成功
drop table if exists t_subpartition_0062_01;
create table t_subpartition_0062_01
(
    col_1 int ,
    col_2 int,
	col_3 varchar2 ( 30 ) ,
    col_4 int
);
--step28: 插入数据; expect:成功
insert into  t_subpartition_0062_01 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step29: 更新指定数据; expect:成功
update t_subpartition_0062_01 set col_2=8 where col_2=4;
--step30: 删除指定数据; expect:成功
delete t_subpartition_0062_01 where col_2=8;

--test5: 一级分区表
drop table if exists t_subpartition_0062_02;
create table t_subpartition_0062_02 (c1 int , c2 int,c3 int )
    partition by range (c2) (
    partition p1 start(1) end(1000) every(200) ,
    partition p2 end(2000),
    partition p3 start(2000) end(2500) ,
    partition p4 start(2500),
    partition p5 start(3000) end(5000) every(1000)
)enable row movement;
--step31: 插入数据; expect:成功
insert into  t_subpartition_0062_02 values (generate_series(0, 19),generate_series(0, 1000));
--step32: 插入数据; expect:成功
insert into t_subpartition_0062_02 values(111,111,111),(2012,222,2012),(301,1111,111),(5050,4060,6060);
--step33: 更新指定数据; expect:成功
update t_subpartition_0062_02 set c1=112 where c1=111;

--step34: 删除表和视图; expect:成功
drop view if exists v_subpartition_0062;
drop materialized view if exists vm_subpartition_0062;
drop table if exists t_subpartition_0062;
drop table if exists t_subpartition_0062_01;
drop table if exists t_subpartition_0062_02;
drop tablespace if exists ts_subpartition_0062;