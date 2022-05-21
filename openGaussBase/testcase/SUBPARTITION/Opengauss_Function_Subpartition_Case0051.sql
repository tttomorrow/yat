-- @testpoint: list_list二级分区表：select,部分测试点合理报错

--test1: select partition/subpartition for
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0051;
drop tablespace if exists ts_subpartition_0051;
create tablespace ts_subpartition_0051 relative location 'subpartition_tablespace/subpartition_tablespace_0051';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0051
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0051
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
insert into t_subpartition_0051 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0051 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0051 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0051 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0051 values(-8,18,1);
--step4: select partition for查询一级分区数据; expect:成功
select * from t_subpartition_0051 partition for (5);
--step5: select subpartition for查询二级分区数据; expect:成功
select * from t_subpartition_0051 subpartition for (5,5);

--test2: select 各种组合
--step6: 查询数据：subpartition/order by/desc; expect:成功
select * from t_subpartition_0051 subpartition(p_list_3_2) order by 1 desc,2;
--step7: 查询数据：subpartition/order by/desc/limit; expect:成功
select * from t_subpartition_0051 subpartition(p_list_3_2) order by 1 desc,2 limit 2,5;
--step8: 查询数据：subpartition/order by/desc/limit/offset; expect:成功
select * from t_subpartition_0051 subpartition(p_list_3_2) order by 1 desc,2 limit 2 offset 3;
--step9: 查询数据：partition/order by/desc/limit/offset; expect:成功
select col_2 from t_subpartition_0051 partition(p_list_1) order by 1 desc limit 2 offset 3;
--step10: 自连接查询数据; expect:成功
select * from t_subpartition_0051  a,t_subpartition_0051 b  where a.col_1=b.col_2 and  a.col_1 >10;
--step11: 子查询查询数据; expect:成功
select * from (select * from t_subpartition_0051 subpartition(p_list_3_2))a,((select * from t_subpartition_0051 subpartition(p_list_1_2))) b  where a.col_1=b.col_2;

--step12: 删除表; expect:成功
drop table if exists t_subpartition_0051;
drop tablespace if exists ts_subpartition_0051;